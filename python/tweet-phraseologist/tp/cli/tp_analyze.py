# coding=utf-8
"""A CLI tool to analyze tweets."""
import argparse


def main() -> None:
    """Parse arguments and call business logic."""
    parser = argparse.ArgumentParser(description='Analyze tweets.')
    args = parser.parse_args()
    print(args)
