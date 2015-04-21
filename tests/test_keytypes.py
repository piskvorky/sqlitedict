# encoding: utf-8
"""
Ensure that types other than 'str' may be used as the dict key.

We make use of 'Test generators' in nose,
https://nose.readthedocs.org/en/latest/writing_tests.html#test-generators

Please note that method generators are not supported in
unittest.TestCase subclasses.
"""

# std imports
import unittest

# local
import sqlitedict
from accessories import TestCaseBackport

def _assert_keyvalue(given_key, given_val):
    # given,
    with sqlitedict.SqliteDict() as db:
        # exercise
        db[given_key] = given_val
        result_key = db.keys()[0]
        result_val = db[result_key]

    # verify
    assert type(result_key) == type(given_key), (result_key, given_key)
    assert type(result_val) == type(given_val), (result_val, given_val)
    assert result_key == given_key, (result_key, given_key)
    assert result_val == given_val, (result_val, given_val)

def test_strtype():
    """ Ensure the default str-type works fine. """
    yield _assert_keyvalue, b'some-key', b'some-val'

class test_nextquery_exception(TestCaseBackport):

    def test_inner_exception(self):
        """Validates that an exception is thrown on *next* query. """
        # per issue #25 we currently expect this to fail, it happens
        # to provide test coverage for the exception handling, however.
        import sqlite3
        # given,
        given_key, given_val = (1, 2), (3, 4)
        with sqlitedict.SqliteDict() as db:
            # exercise
            db[given_key] = given_val
            with self.assertRaises(sqlite3.InterfaceError):
                result_key = db.keys()[0]
