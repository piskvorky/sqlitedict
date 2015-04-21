"""Accessories for test cases."""
# std imports
import unittest
import contesxtlib
import os
import sys

def norm_file(fname):
    """Normalize test filename, creating a directory path to it if necessary"""
    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return fname


class TestCaseBackport(unittest.TestCase):
    """Backport unittest.TestCase.assertRaises for python2.5 and 2.6."""
    if sys.version_info < (2, 7):
        @contextlib.contextmanager
        def assertRaises(self, excClass):
            try:
                yield
            except Exception as e:
                assert isinstance(e, excClass)
            else:
                raise AssertionError("%s was not raised" % excClass)

        @contextlib.contextmanager
        def assertRaisesRegexp(self, excClass, pattern):
            import re
            try:
                yield
            except Exception as e:
                assert isinstance(e, excClass)
                assert re.match(pattern, str(e))
            else:
                raise AssertionError("%s was not raised" % excClass)



