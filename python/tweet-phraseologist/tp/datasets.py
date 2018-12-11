# coding=utf-8
"""Tools for working with datasets."""
import abc
import csv
import importlib
import multiprocessing
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePath
from typing import IO, List, Mapping, Optional, Set, Tuple

import pkg_resources
from xdg import BaseDirectory

from tp import exceptions
from tp.constants import ARCHIVES_DIR, DATASETS_DIR


class Dataset(abc.ABC):
    """A dataset.

    A dataset is a corpus of tweets, plus useful metadata such as each tweet's
    author and party affiliation. This class represents a generic dataset, and
    provides tools for working with it.

    This class is abstract. Subclasses provide dataset-specific logic.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return this dataset's name.

        This name is used when generating filesystem path names. As a result,
        it's strongly recommended to use a restricted set of characters, such
        as ``a-zA-Z-_.``.
        """

    @abc.abstractmethod
    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        The exact procedure for installing a dataset varies depending on the
        dataset at hand. Subclasses (which represent specific datasets) must
        provide this logic. As an example, a subclass might implement the
        following installation procedure:

        1. Check if the dataset is already installed. If so, return. (See
           :func:`tp.datasets.installed`.)
        2. If an ``archive`` hasn't been provided, download one into an
           :data:`tp.constants.ARCHIVES_DIR`.
        3. Extract the archive into a :data:`tp.constants.DATASETS_DIR`.

        :param archive: The path to a zip archive containing the dataset.
        """

    def installed(self) -> bool:
        """Tell whether this dataset is installed.

        :return: True if this dataset is installed, false otherwise.
        """
        try:
            self.install_path()
        except exceptions.DatasetNotFoundError:
            return False
        return True

    def install_path(self) -> Path:
        """Return the path to where this dataset is installed.

        :return: The path to where this dataset is installed.
        :raise tp.exceptions.DatasetNotFoundError: If the dataset is not
            installed.
        """
        importlib.reload(BaseDirectory)
        for datasets_dir in BaseDirectory.load_data_paths(DATASETS_DIR):
            candidate_path = Path(datasets_dir, self.name)
            if candidate_path.exists():
                return candidate_path
        raise exceptions.DatasetNotFoundError(
            f"Dataset {self.name} isn't installed."
        )

    def uninstall(self) -> None:
        """Uninstall this dataset.

        :raise tp.exceptions.DatasetNotFoundError: If the dataset to uninstall
            is not currently installed.
        """
        shutil.rmtree(self.install_path())


class DVRTDataset(Dataset):
    """The `democratsvsrepublicantweets`_ dataset.

    .. _democratsvsrepublicantweets:
        https://www.kaggle.com/kapastor/democratvsrepublicantweets
    """

    _trunc_matcher = re.compile(r'(.+)\s+\S*…', flags=re.DOTALL)
    _url_matcher = re.compile(r'\s+https://t.co/\S+')

    @property
    def archive(self) -> str:
        """Return the name of the archive containing this dataset."""
        return self.name + '.zip'

    @property
    def name(self) -> str:
        """Return this dataset's name.

        For more information, see :meth:`tp.datasets.Dataset.name`.
        """
        return 'democratvsrepublicantweets'

    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        :param archive: The path to a zip archive containing the dataset.
        :raise DatasetInstallError: If no ``archive`` is provided and none is
            found in TP's cache.
        """
        if self.name in installed():
            return
        importlib.reload(BaseDirectory)
        dst = Path(BaseDirectory.save_data_path(DATASETS_DIR), self.name)
        assert not dst.exists()

        # Decide on an archive to extract.
        if not archive:
            archive = Path(
                BaseDirectory.xdg_cache_home,
                ARCHIVES_DIR,
                self.archive,
            )
            if not archive.exists():
                raise exceptions.DatasetInstallError(
                    'No archive explicitly provided, and none found at '
                    f"{archive}. Can't install this dataset."
                )

        tmp = tempfile.mkdtemp()
        try:
            # Extract archive.
            with zipfile.ZipFile(archive, 'r') as handle:
                handle.extractall(tmp)

            # Fix TwitterHandles.csv.
            infile_path = Path(tmp, 'TwitterHandles.csv')
            outfile_path = Path(tmp, 'FixedTwitterHandles.csv')
            with open(infile_path) as infile:
                with open(outfile_path, 'w') as outfile:
                    self.munge_twitter_handles(infile, outfile)
            shutil.move(outfile_path, infile_path)

            # Fix ExtractedTweets.csv.
            infile_path = Path(tmp, 'ExtractedTweets.csv')
            outfile_path = Path(tmp, 'FixedExtractedTweets.csv')
            with open(infile_path) as infile:
                with open(outfile_path, 'w') as outfile:
                    self.munge_extracted_tweets(infile, outfile)
            shutil.move(outfile_path, infile_path)

            # Install fixed files.
            shutil.move(tmp, dst)
        except:
            shutil.rmtree(tmp)
            raise

    @staticmethod
    def munge_twitter_handles(infile: IO[str], outfile: IO[str]) -> None:
        """Fix the ``TwitterHandles.csv`` file.

        The file contains some rows that differ only in having different avatar
        URLs. For example::

            Democrat,Adriano Espaillat,RepEspaillat,https…/RJ5H4gCN_bigger.jpg
            Democrat,Adriano Espaillat,RepEspaillat,https…/RJ5H4gCN_normal.jpg

        Filter these out.

        :param infile: The file to read and fix.
        :param outfile: The fixed file to write to.
        """
        handles: Set[str] = set()
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for i, row in enumerate(reader):
            # write header row
            if i == 0:
                writer.writerow(row)
                continue

            # drop duplicate-ish row
            handle = row[2]
            if handle in handles:
                continue
            handles.add(handle)

            # write original row
            writer.writerow(row)

    @classmethod
    def munge_extracted_tweets(cls, infile: IO[str], outfile: IO[str]) -> None:
        """Fix the ``ExtractedTweets.csv`` file.

        The file contains many truncated tweets, ending with text such as the
        following::

            here in the House… https://t.co/n3tggDLU1L
            National Teacher Apprecia…

        These suffixes harm subsequent analyses, by making tasks such sentence
        splitting, word splitting and stemming harder. Address this by
        stripping said text. The above lines are fixed to end with::

            here in the
            National Teacher

        In addition, URLs are embedded in many tweets, like this::

            Deep bow from a Cavs fan! https://t.co/BD0xOh6TB3

        Drop these URLs. The above would be changed to:

            Deep bow from a Cavs fan!

        This has the potential to screw up some legitimate tweets and drop a
        few complete words, but short of getting a better dataset that doesn't
        truncate tweets and append tweet URLs, this seems like a reasonable
        solution.
        """
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(next(reader))  # write header row
        with multiprocessing.Pool() as pool:
            # Chunksize chosen empirically with an R7 1700 CPU.
            # imap_unordered() used because row ordering doesn't affect
            # correctness and ignoring ordering can improve performance.
            for row in pool.imap_unordered(
                    func=cls.munge_row,
                    iterable=reader,
                    chunksize=2**8):
                writer.writerow(row)

    @classmethod
    def munge_row(cls, row: List[str]) -> Tuple[str, ...]:
        """Fix the tweet in the given row.

        For details, see :meth:`munge_extracted_tweets`.
        """
        # Mutating `row` might be more efficient, but mutating inputs can cause
        # hard-to-understand bugs. Better to work on a solution which avoids
        # this issue, such as making it so that this method only accepted and
        # returned a tweet.
        old_tweet = row[-1]
        truncated = re.search(cls._trunc_matcher, old_tweet)
        if truncated:
            new_tweet = truncated.group(1)
        else:
            new_tweet = old_tweet
        new_tweet = re.sub(cls._url_matcher, '', new_tweet)
        return tuple(row[:-1]) + (new_tweet,)


class SimpleFixtureDataset(Dataset):
    """A subset of :class:`DVTRDataset` for testing purposes."""

    @property
    def name(self) -> str:
        """Return this dataset's name.

        For more information, see :meth:`tp.datasets.Dataset.name`.
        """
        return 'simple-fixture'

    def install(self, archive: Optional[Path] = None) -> None:
        """Install this dataset.

        :param archive: **Ignored.**
        """
        if self.name in installed():
            return
        importlib.reload(BaseDirectory)
        dst = Path(BaseDirectory.save_data_path(DATASETS_DIR), self.name)
        assert not dst.exists()

        tmp = tempfile.mkdtemp()
        try:
            for name in ('ExtractedTweets.csv', 'TwitterHandles.csv'):
                in_path = str(PurePath('static', 'simple-fixture', name))
                out_path = str(PurePath(tmp, name))
                with pkg_resources.resource_stream('tp', in_path) as in_handle:
                    with open(out_path, 'wb') as out_handle:
                        shutil.copyfileobj(in_handle, out_handle)
            shutil.copytree(tmp, dst)
        except:
            shutil.rmtree(tmp)
            raise


def installed() -> Mapping[str, Path]:
    """Get currently installed datasets.

    :return: A mapping in the form ``{dataset_name: dataset_path}``.
    """
    result = {}
    importlib.reload(BaseDirectory)
    for datasets_dir in BaseDirectory.load_data_paths(DATASETS_DIR):
        for dataset_dir in Path(datasets_dir).glob('*'):
            result[dataset_dir.name] = dataset_dir
    return result


def manageable() -> Mapping[str, Dataset]:
    """Get manageable datasets.

    :return: A mapping in the form ``datset_name: dataset_obj}``.
    """
    return {
        obj.name: obj
        for obj in (DVRTDataset(), SimpleFixtureDataset())
    }
