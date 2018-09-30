# coding=utf-8
"""Tools for creating and using personalized predictors for users."""
import functools
import multiprocessing

from movie_recommender import db, exceptions
from movie_recommender.constants import GENRES
from movie_recommender.graph import Graph, Point


def analyze_users(user_ids, overwrite, jobs):
    """Analyze users, to find out which predictor works best for them.

    :param user_ids: An iterable of user IDs. The users for which analyses are
        being performed.
    :param overwrite: If a user has already been analyzed, should the analysis
        be overwritten?
    :param jobs: The number of processes to spawn. If none, spawn one per CPU.
    :returns: Nothing.
    """
    pfu_args = tuple((user_id, overwrite) for user_id in user_ids)
    with multiprocessing.Pool(jobs) as pool:
        pool.starmap(analyze_user, pfu_args)


def analyze_user(user_id, overwrite):
    """Analyze a user, to find out which predictor works best for them.

    :param user_id: A user ID. The user for which an analysis is being
        performed.
    :param overwrite: If a user has already been analyzed, should the analysis
        be overwritten?
    :returns: Nothing.
    """
    with db.get_db_conn(db.get_load_path()) as conn:
        # Does this user already have a personalized predictor?
        if not overwrite and conn.execute(
                'SELECT * FROM predictors WHERE userId=?',
                (user_id,)).fetchall():
            return

        # Create a personalized predictor for this user. SQLite added
        # support for UPSERT in version 3.24.0, which was released on
        # 2018-06-24. See: https://www.sqlite.org/lang_UPSERT.html
        sses = calc_sse(user_id)
        predictor = min_sse(sses)
        with conn:
            conn.execute(
                """
                INSERT INTO predictors VALUES (?, ?)
                ON CONFLICT (userId) DO UPDATE SET predictor=?
                """,
                (user_id, predictor, predictor)
            )


def calc_sse(user_id):
    """Calculate the SSE for each type of predictor for the given user.

    .. WARNING:: This function may take a long time to execute.

    :param user_id: A user ID.
    :return: A dict in the form ``{predictor_name: sum_of_squared_errors}``.
    """
    sses = {}  # predictor name → sum of squared errors
    movie_ids = db.get_rated_movies(user_id)

    # Repeatedly select one movie to serve as the control, and make predictors
    # from the remaining movies.
    for movie_id in movie_ids:
        predictors = {'year': make_year_predictor(user_id, movie_id)}
        for genre in GENRES:
            predictors[f'genre:{genre}'] = (
                make_genre_predictor(genre, user_id, movie_id)
            )

        # See how well each predictor predicts the control. If we're using a
        # year-based predictor, then two errors can occur:
        #
        # * The movie for which a prediction is being made doesn't have a
        #   year.
        # * The movie for which a prediction is being made does have a
        #   year, but all of the _other_ movies the user has rated don't
        #   have a year.
        #
        # In either case, we respond by not calculating an SSE for the
        # predictor.
        #
        # It is possible to encounter this problem for every combination of
        # (control movie, other movies) for a user. In this case, we set the
        # SSE for that type of predictor to "infinite." Other areas of the code
        # base must be prepared to find out that a predictor has an infinite
        # SSE.
        for pred_name, pred in predictors.items():
            try:
                predicted_rating = pred(movie_id)
            except (exceptions.NoMovieYearError, exceptions.EmptyGraphError):
                continue
            actual_rating = db.get_rating(user_id, movie_id)
            sses.setdefault(pred_name, 0)
            sses[pred_name] += (predicted_rating - actual_rating) ** 2

    sses.setdefault('year', float('inf'))
    return sses


def min_sse(sses):
    """Select the best predictor from the given choices.

    :param sses: A dict in the form ``{predictor_name:
        sum_of_squared_errors}``.
    :return: A predictor name.
    """
    best_pred_name, best_sse = sses.popitem()
    while sses:
        pred_name, sse = sses.popitem()
        if sse < best_sse:
            best_pred_name, best_sse = pred_name, sse
    return best_pred_name


def clamp_rating(rating):
    """Clamp the given movie rating to the range [0.5, 5].

    :param rating: A movie rating.
    :return: The given movie rating, but clamped.
    """
    return max(0.5, min(5, rating))


def make_predictor(user_id, predictor_name):
    """Make a univariate predictor for the given user.

    :param user_id: A user ID. The user for which a predictor is being created.
    :param predictor_name: The type of predictor to create. Defines whether the
        predictor will use year, comedy genre, horror genre, etc when making
        predictions.
    :return: A predictor. A function which accepts a movie ID and returns a
        rating.
    """
    predictor_factory = get_predictor_factory(predictor_name)
    return predictor_factory(user_id)


def get_predictor_factory(predictor_name):
    """Find the appropriate predictor factory function.

    :param predictor_name: The desired type of predictor. For example, "year"
        or "genre:Animation."
    :return: A predictor factor function, such as
        :func:`movie_recommender.predict.make_year_predictor`. A predictor
        factory function is one which accepts a ``user_id`` argument and
        returns a predictor function customized for that user.
    :raise movie_recommender.exceptions.NoSuchPredictorError: If the requested
        type of predictor is not yet implemented.
    """
    predictor_factories = {'year': make_year_predictor}
    for genre in GENRES:
        predictor_factories[f'genre:{genre}'] = (
            functools.partial(make_genre_predictor, genre)
        )
    try:
        return predictor_factories[predictor_name]
    except KeyError:
        raise exceptions.NoSuchPredictorError(
            f'A predictor for {predictor_name} is not (yet) implemented.'
        )


def make_year_predictor(user_id, forbidden_movie=None):
    """Make a year-based predictor for the given user.

    If year information can't be extracted from a movie's title, then that
    movie is skipped when generating a predictor. This is done because so few
    movies have this issue. See:
    `class:`movie_recommender.exceptions.NoMovieYearError`.

    :param user_id: A user ID. The user for which a predictor is being created.
    :param forbidden_movie: A movie ID. A movie to ignore when creating the
        predictor.
    :return: A function which accepts a movie ID and returns a predicted
        rating.
    """
    query = """
            SELECT movies.title, ratings.rating
            FROM movies JOIN ratings USING (movieId)
            WHERE ratings.userId == ?
            """
    params = [user_id]
    if forbidden_movie:
        query += 'AND movieId != ?'
        params.append(forbidden_movie)

    # Iterate through movies this user has rated. For each movie, create a
    # Cartesian point, where X is the movie's year, and Y is the rating this
    # user has given to this movie.
    points = []
    with db.get_db_conn(db.get_load_path()) as conn:
        for row in conn.execute(query, params):
            try:
                year = db.get_year(row[0])
            except exceptions.NoMovieYearError:
                continue
            rating = row[1]
            points.append(Point(year, rating))
    graph = Graph(points)

    def predictor(movie_id):
        """Predict a user's rating for the given movie.

        :param movie_id: A movie ID.
        :return: A predicted rating for the given movie.
        :raise movie_recommender.exceptions.NoMovieYearError: If the given
            movie's title doesn't include a year, and this predictor makes use
            of year data.
        :raise movie_recommender.exceptions.EmptyGraphError: If this predictor
            can't predict movie ratings at all, due to a lack of relevant data.
            For example, this will occur if the given movie's title does
            include a year, but all of the movies this user has rated lack a
            year.
        """
        title = db.get_title(movie_id)
        year = db.get_year(title)
        try:
            rating = graph.predict_y(year)
        except exceptions.VerticalLineOfBestFitGraphError:
            rating = graph.avg_point.y
        return clamp_rating(rating)

    return predictor


def make_genre_predictor(genre, user_id, forbidden_movie=None):
    """Make a predictor for the given genre for the given user.

    :param genre: A genre name, as a string.
    :param user_id: A user ID. The user for which a predictor is being created.
    :param forbidden_movie: A movie ID. A movie to ignore when creating the
        predictor.
    :return: A function which accepts a movie ID and returns a predicted
        rating.
    """
    query = """
            SELECT movies.genres, ratings.rating
            FROM movies JOIN ratings USING (movieId)
            WHERE ratings.userId == ?
            """
    params = [user_id]
    if forbidden_movie:
        query += 'AND movieId != ?'
        params.append(forbidden_movie)

    # Iterate through movies this user has rated. For each movie, create a
    # Cartesian point, where X is whether the move has the given genre, and Y
    # is the rating this user has given to this movie.
    points = []
    with db.get_db_conn(db.get_load_path()) as conn:
        for row in conn.execute(query, params):
            genres = row[0].split('|')
            genre_present = 1 if genre in genres else 0
            rating = row[1]
            points.append(Point(genre_present, rating))
    graph = Graph(points)

    def predictor(movie_id):
        """Predict a user's rating for the given movie.

        :param movie_id: A movie ID.
        :return: A predicted rating for the given movie.
        """
        genres = db.get_genres(movie_id)
        genre_present = 1 if genre in genres else 0
        try:
            rating = graph.predict_y(genre_present)
        except exceptions.VerticalLineOfBestFitGraphError:
            rating = graph.avg_point.y
        return clamp_rating(rating)

    return predictor
