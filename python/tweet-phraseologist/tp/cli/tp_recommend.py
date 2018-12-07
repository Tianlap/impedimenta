# coding=utf-8
"""A CLI tool to recommend common phrases."""
import argparse


def main() -> None:
    """Parse arguments and call business logic."""
    parser = argparse.ArgumentParser(description='Recommend common phrases.')
    args = parser.parse_args()
    print(args)
