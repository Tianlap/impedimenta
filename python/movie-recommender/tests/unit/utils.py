# coding=utf-8
"""Utilities for unit tests."""
import os


def get_fixture(filename):
    """Generate the path to a file in the "fixtures" directory."""
    return os.path.join(os.path.dirname(__file__), 'fixtures', filename)
