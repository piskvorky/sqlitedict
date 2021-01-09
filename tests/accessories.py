"""Accessories for test cases."""
import os


def norm_file(fname):
    """Normalize test filename, creating a directory path to it if necessary"""
    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return fname
