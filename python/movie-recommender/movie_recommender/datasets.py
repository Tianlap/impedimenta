# coding=utf-8
"""Tools for working with Movie Recommender's datasets."""
import os
import zipfile
from urllib.parse import urlsplit

import requests
from xdg import BaseDirectory

from movie_recommender import exceptions
from movie_recommender.constants import DATASETS, XDG_RESOURCE


class Dataset():
    """An interface to a :data:`movie_recommender.constants.DATASETS`."""

    def __init__(self, name):
        """Initialize this object.

        :param name: A key from :data:`movie_recommender.constants.DATASET`.
        :raise: ValueError if an invalid name is given.
        """
        if name not in DATASETS:
            raise ValueError(
                "This application doesn't know how to manage a dataset named "
                '{}. Only the following may be managed: {}'
                .format(
                    name,
                    ', '.join((str(key) for key in DATASETS))
                )
            )
        self.name = name

    def download(self):
        """Download this dataset into the application cache directory.

        Short circuit if the dataset is "fixture," or if the dataset is already
        downloaded.

        :return: Nothing.
        """
        if self.name == 'fixture':
            return
        cache_dir = BaseDirectory.save_cache_path(XDG_RESOURCE)
        archive_url = DATASETS[self.name]
        archive_basename = os.path.basename(urlsplit(archive_url).path)
        archive_path = os.path.join(cache_dir, archive_basename)
        if os.path.exists(archive_path):
            return
        with open(archive_path, 'wb') as handle:
            # The chunk size of 256 bytes (2^8) is arbitrarily chosen.
            for chunk in requests.get(archive_url).iter_content(chunk_size=256):
                handle.write(chunk)

    def download_path(self):
        """Return the path to where this dataset is downloaded.

        :return: The path to where this dataset is downloaded.
        :raise movie_recommender.exceptions.DatasetAbsentError: If this
            dataset's name is "fixture."
        """
        if self.name == 'fixture':
            raise exceptions.DatasetAbsentError(
                f"Dataset {self.name} can't be downloaded."
            )
        cache_dir = os.path.join(BaseDirectory.xdg_cache_home, XDG_RESOURCE)
        archive_url = DATASETS[self.name]
        archive_basename = os.path.basename(urlsplit(archive_url).path)
        archive_path = os.path.join(cache_dir, archive_basename)
        if not os.path.exists(archive_path):
            raise exceptions.DatasetAbsentError(
                f'Dataset {self.name} is not downloaded.'
            )
        return archive_path

    def downloaded(self):
        """Tell whether this dataset is downloaded.

        :return: True if this dataset is downloaded, false otherwise.
        """
        try:
            self.download_path()
            return True
        except exceptions.DatasetAbsentError:
            return False

    def install(self):
        """Install this dataset.

        Short circuit if this dataset is already installed.

        :return: Nothing.
        """
        if self.name == 'fixture':
            self._install_fixture()
            return
        if self.installed():
            return
        download_path = self.download_path()
        data_dir = BaseDirectory.save_data_path(XDG_RESOURCE)
        with zipfile.ZipFile(download_path, 'r') as handle:
            handle.extractall(data_dir)

    def _install_fixture(self):
        """Install the "fixture" dataset.

        Short circuit if this dataset is already installed.

        :return: Nothing.
        """
        if self.installed():
            return
        data_dir = BaseDirectory.save_data_path(XDG_RESOURCE)
        fixture_dir = os.path.join(data_dir, self.name)
        os.mkdir(fixture_dir)
        _write_links_csv(os.path.join(fixture_dir, 'links.csv'))
        _write_movies_csv(os.path.join(fixture_dir, 'movies.csv'))
        _write_ratings_csv(os.path.join(fixture_dir, 'ratings.csv'))
        _write_tags_csv(os.path.join(fixture_dir, 'tags.csv'))

    def install_path(self):
        """Return the path to where this dataset is installed.

        :return: The path to where this dataset is installed.
        :raise movie_recommender.exceptions.DatasetAbsentError: If the
            dataset is not installed.
        """
        for data_dir in BaseDirectory.load_data_paths(XDG_RESOURCE):
            candidate_path = os.path.join(data_dir, self.name)
            if os.path.exists(candidate_path):
                return candidate_path
        raise exceptions.DatasetAbsentError(
            f'Dataset {self.name} is not installed.'
        )

    def installed(self):
        """Tell whether this dataset is installed.

        :return: True if this dataset is installed, false otherwise.
        """
        try:
            self.install_path()
            return True
        except exceptions.DatasetAbsentError:
            return False


def get_installed_datasets():
    """Tell which datasets are installed.

    :return: A dict in the form ``{dataset_name: dataset_path}``.
    """
    paths = {}
    for dataset_name in DATASETS:
        dataset = Dataset(dataset_name)
        if dataset.installed():
            paths[dataset_name] = dataset.install_path()
    return paths


def _write_links_csv(path):
    """Write a bogus "links.csv" file.

    :param path: The path to where the bogus file should be written.
    :return: Nothing.
    """
    with open(path, 'w') as handle:
        handle.write('movieId,imdbId,tmdbId\n')
        handle.write('1,0000000,000\n')
        handle.write('2,1111111,0001\n')
        handle.write('3,2222222,0010\n')
        handle.write('4,3333333,0011\n')


def _write_movies_csv(path):
    """Write a bogus "movies.csv" file.

    :param path: The path to where the bogus file should be written.
    :return: Nothing.
    """
    with open(path, 'w') as handle:
        handle.write('movieId,title,genres\n')

        # Movies users may have rated
        handle.write('1,Foo (1960),Animation|Children\n')
        handle.write('2,Bar (1970),Animation|Horror\n')
        handle.write('3,Biz (1980),(no genres listed)\n')
        handle.write('4,Baz,(no genres listed)\n')
        handle.write('5,Boo,(no genres listed)\n')

        # Movies users haven't rated
        handle.write('10,One (1950),Children\n')
        handle.write('11,Two (1990),Animation\n')
        handle.write('12,Three,Horror\n')
        handle.write('13,Four,(no genres listed)\n')


def _write_ratings_csv(path):
    """Write a bogus "ratings.csv" file.

    :param path: The path to where the bogus file should be written.
    :return: Nothing.
    """
    with open(path, 'w') as handle:
        handle.write('userId,movieId,rating,timestamp\n')

        # Best predictor: genre:Animation
        handle.write('1,1,4.0,123456789\n')
        handle.write('1,2,5.0,1234567890\n')
        handle.write('1,3,0.5,123456789\n')
        handle.write('1,4,1.5,1234567890\n')

        # Best predictor: year
        # Inverse linear relationship between year and rating.
        handle.write('2,1,3.5,123456789\n')
        handle.write('2,2,3.0,123456789\n')
        handle.write('2,3,2.5,123456789\n')
        handle.write('2,4,3.0,123456789\n')

        # Best predictor: genre:(no genres listed)
        # All of the movies this user has rated have the `genre:(no genres
        # listed)` genre. As a result, the scatter plot is a vertical line, and
        # the recommendation is the average of ratings: 3.5.
        handle.write('3,3,2.0,123456789\n')
        handle.write('3,4,5.0,123456789\n')

        # Best predictor: (no genres listed)
        # The user hasn't rated any movies with year data, so the SSE for a
        # year-based predictor is infinite.
        handle.write('4,4,4.0,123456789\n')
        handle.write('4,5,5.0,123456789\n')


def _write_tags_csv(path):
    """Write a bogus "tags.csv" file.

    :param path: The path to where the bogus file should be written.
    :return: Nothing.
    """
    with open(path, 'w') as handle:
        handle.write('userId,movieId,tag,timestamp\n')
        handle.write('2,60756,funny,1445714994\n')
        handle.write('2,60756,Highly quotable,1445714996\n')
