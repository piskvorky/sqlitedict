"""Accessories for test cases."""
# std imports
import unittest
import contextlib
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
    """Backport python2.7 TestCase methods (in leiu of unittest2, or better, pytest)."""
    if sys.version_info < (2, 7):

        def assertNotIn(self, member, container, msg=None):
            """Just like self.assertTrue(a not in b), but with a nicer default message."""
            if member in container:
                standardMsg = '%s unexpectedly found in %s' % (safe_repr(member),
                                                            safe_repr(container))
                self.fail(self._formatMessage(msg, standardMsg))

        def assertIn(self, member, container, msg=None):
            """Just like self.assertTrue(a in b), but with a nicer default message."""
            if member not in container:
                standardMsg = '%s not found in %s' % (safe_repr(member),
                                                      safe_repr(container))
                self.fail(self._formatMessage(msg, standardMsg))

        def assertIs(self, expr1, expr2, msg=None):
            """Just like self.assertTrue(a is b), but with a nicer default message."""
            if expr1 is not expr2:
                standardMsg = '%s is not %s' % (safe_repr(expr1),
                                                 safe_repr(expr2))
                self.fail(self._formatMessage(msg, standardMsg))


        def assertIsInstance(self, obj, cls, msg=None):
            """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
            default message."""
            if not isinstance(obj, cls):
                standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
                self.fail(self._formatMessage(msg, standardMsg))

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
