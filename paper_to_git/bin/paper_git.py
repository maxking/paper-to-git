"""The paper_git command dispatcher"""


import argparse

from paper_to_git.core import initialize


def main():
    """The `paper_git command dispatcher."""
    parser = argparse.ArgumentParser(description="""\
    The Paper-to-Git system
    Copyright 2017 Abhilash Raj""",
    formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()
    initialize()
    print("Initialization Done!")
