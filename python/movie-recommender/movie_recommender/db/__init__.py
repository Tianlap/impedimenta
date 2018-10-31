# coding=utf-8
"""Tools for working with Movie Recommender's database.

There are *numerous* functions for working with Movie Recommender's database.
The functions are split into themed modules, to ease the burden of navigation.

Many of the functions in this module return a set of results from the database,
instead of a generator yielding results from the database. It's typically
preferable to implement functions like this as a generator. But in SQLite,
reads block writes, and keeping connections open will cause pending writes to
time out.

A better solution is to implement such functions as generators, and to ask
callers to worry about issues like immediately draining generators, or using
them as intended and cleanly separating reads from writes. But this solution
will require code re-writes, and such re-writes haven't yet been done.
"""
