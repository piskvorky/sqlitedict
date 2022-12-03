# std imports
import json
import unittest
import tempfile
import os
from unittest.mock import patch

# local
import sqlitedict
from sqlitedict import SqliteDict
from test_temp_db import TempSqliteDictTest
from accessories import norm_file


class SqliteMiscTest(unittest.TestCase):

    def test_with_statement(self):
        """Verify using sqlitedict as a contextmanager . """
        with SqliteDict() as d:
            self.assertTrue(isinstance(d, SqliteDict))
            self.assertEqual(dict(d), {})
            self.assertEqual(list(d), [])
            self.assertEqual(len(d), 0)

    def test_reopen_conn(self):
        """Verify using a contextmanager that a connection can be reopened."""
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        db = SqliteDict(filename=fname)
        with db:
            db['key'] = 'value'
            db.commit()
        with db:
            db['key'] = 'value'
            db.commit()

    def test_as_str(self):
        """Verify SqliteDict.__str__()."""
        # given,
        db = SqliteDict()
        # exercise
        db.__str__()
        # test when db closed
        db.close()
        db.__str__()

    def test_as_repr(self):
        """Verify SqliteDict.__repr__()."""
        # given,
        db = SqliteDict()
        # exercise
        db.__repr__()

    def test_directory_notfound(self):
        """Verify RuntimeError: directory does not exist."""
        # given: a non-existent directory,
        folder = tempfile.mkdtemp(prefix='sqlitedict-test')
        os.rmdir(folder)
        # exercise,
        with self.assertRaises(RuntimeError):
            SqliteDict(filename=os.path.join(folder, 'nonexistent'))

    def test_commit_nonblocking(self):
        """Coverage for non-blocking commit."""
        # given,
        with SqliteDict(autocommit=True) as d:
            # exercise: the implicit commit is nonblocking
            d['key'] = 'value'
            d.commit(blocking=False)

    def test_cancel_iterate(self):
        import time

        class EndlessKeysIterator:
            def __init__(self) -> None:
                self.value = 0

            def __iter__(self):
                return self

            def __next__(self):
                self.value += 1
                return [self.value]

        with patch('sqlitedict.sqlite3') as mock_sqlite3:
            ki = EndlessKeysIterator()
            cursor = mock_sqlite3.connect().cursor()
            cursor.__iter__.return_value = ki

            with SqliteDict(autocommit=True) as d:
                for i, k in enumerate(d.keys()):
                    assert i + 1 == k
                    if k > 100:
                        break
                assert ki.value > 101

                # Release GIL, let background threads run.
                # Don't use gc.collect because this is simulate user code.
                time.sleep(0.01)

                current = ki.value
                time.sleep(1)
                assert current == ki.value, 'Will not read more after iterate stop'


class NamedSqliteDictCreateOrReuseTest(TempSqliteDictTest):
    """Verify default flag='c', and flag='n' of SqliteDict()."""

    def test_default_reuse_existing_flag_c(self):
        """Re-opening of a database does not destroy it."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db = SqliteDict(filename=fname)
        orig_db['key'] = 'value'
        orig_db.commit()
        orig_db.close()

        next_db = SqliteDict(filename=fname)
        self.assertIn('key', next_db.keys())
        self.assertEqual(next_db['key'], 'value')

    def test_overwrite_using_flag_n(self):
        """Re-opening of a database with flag='c' destroys it all."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db = SqliteDict(filename=fname, tablename='sometable')
        orig_db['key'] = 'value'
        orig_db.commit()
        orig_db.close()

        # verify,
        next_db = SqliteDict(filename=fname, tablename='sometable', flag='n')
        self.assertNotIn('key', next_db.keys())

    def test_unrecognized_flag(self):

        def build_with_bad_flag():
            fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
            SqliteDict(filename=fname, flag='FOO')

        with self.assertRaises(RuntimeError):
            build_with_bad_flag()

    def test_readonly(self):
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db = SqliteDict(filename=fname)
        orig_db['key'] = 'value'
        orig_db['key_two'] = 2
        orig_db.commit()
        orig_db.close()

        readonly_db = SqliteDict(filename=fname, flag='r')
        self.assertTrue(readonly_db['key'] == 'value')
        self.assertTrue(readonly_db['key_two'] == 2)

        def attempt_write():
            readonly_db['key'] = ['new_value']

        def attempt_update():
            readonly_db.update(key='value2', key_two=2.1)

        def attempt_delete():
            del readonly_db['key']

        def attempt_clear():
            readonly_db.clear()

        def attempt_terminate():
            readonly_db.terminate()

        attempt_funcs = [attempt_write, attempt_update, attempt_delete, attempt_clear, attempt_terminate]

        for func in attempt_funcs:
            with self.assertRaises(RuntimeError):
                func()

    def test_readonly_table(self):
        """
        Read-only access on a non-existent tablename should raise RuntimeError,
        and not create a new (empty) table.
        """
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        dummy_tablename = 'table404'
        orig_db = SqliteDict(filename=fname)
        orig_db['key'] = 'value'
        orig_db['key_two'] = 2
        orig_db.commit()
        orig_db.close()

        self.assertFalse(dummy_tablename in SqliteDict.get_tablenames(fname))

        with self.assertRaises(RuntimeError):
            SqliteDict(filename=fname, tablename=dummy_tablename, flag='r')

        self.assertFalse(dummy_tablename in SqliteDict.get_tablenames(fname))

    def test_irregular_tablenames(self):
        """Irregular table names need to be quoted"""
        def __test_irregular_tablenames(tablename):
            filename = ':memory:'
            db = SqliteDict(filename, tablename=tablename)
            db['key'] = 'value'
            db.commit()
            self.assertEqual(db['key'], 'value')
            db.close()

        __test_irregular_tablenames('9nine')
        __test_irregular_tablenames('outer space')
        __test_irregular_tablenames('table with a "quoted" name')
        __test_irregular_tablenames("table with a \"quoted \xe1cute\" name")

    def test_overwrite_using_flag_w(self):
        """Re-opening of a database with flag='w' destroys only the target table."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db_1 = SqliteDict(filename=fname, tablename='one')
        orig_db_1['key'] = 'value'
        orig_db_1.commit()
        orig_db_1.close()

        orig_db_2 = SqliteDict(filename=fname, tablename='two')
        orig_db_2['key'] = 'value'
        orig_db_2.commit()
        orig_db_2.close()

        # verify, when re-opening table space 'one' with flag='2', we destroy
        # its contents.  However, when re-opening table space 'two' with
        # default flag='r', its contents remain.
        next_db_1 = SqliteDict(filename=fname, tablename='one', flag='w')
        self.assertNotIn('key', next_db_1.keys())

        next_db_2 = SqliteDict(filename=fname, tablename='two')
        self.assertIn('key', next_db_2.keys())


class SqliteDictTerminateTest(unittest.TestCase):

    def test_terminate_instead_close(self):
        ''' make terminate() instead of close()
        '''
        d = sqlitedict.open('tests/db/sqlitedict-terminate.sqlite')
        d['abc'] = 'def'
        d.commit()
        self.assertEqual(d['abc'], 'def')
        d.terminate()
        self.assertFalse(os.path.isfile('tests/db/sqlitedict-terminate.sqlite'))


class SqliteDictTerminateFailTest(unittest.TestCase):
    """Provide Coverage for SqliteDict.terminate()."""

    def setUp(self):
        self.fname = norm_file('tests/db-permdenied/sqlitedict.sqlite')
        self.db = SqliteDict(filename=self.fname)
        os.chmod(self.fname, 0o000)
        os.chmod(os.path.dirname(self.fname), 0o000)

    def tearDown(self):
        os.chmod(os.path.dirname(self.fname), 0o700)
        os.chmod(self.fname, 0o600)
        os.unlink(self.fname)
        os.rmdir(os.path.dirname(self.fname))

    def test_terminate_cannot_delete(self):
        # exercise,
        self.db.terminate()  # deletion failed, but no exception raised!

        # verify,
        os.chmod(os.path.dirname(self.fname), 0o700)
        os.chmod(self.fname, 0o600)
        self.assertTrue(os.path.exists(self.fname))


class SqliteDictJsonSerializationTest(unittest.TestCase):
    def setUp(self):
        self.fname = norm_file('tests/db-json/sqlitedict.sqlite')
        self.db = SqliteDict(
            filename=self.fname, tablename='test', encode=json.dumps, decode=json.loads
        )

    def tearDown(self):
        self.db.close()
        os.unlink(self.fname)
        os.rmdir(os.path.dirname(self.fname))

    def get_json(self, key):
        return self.db.conn.select_one('SELECT value FROM test WHERE key = ?', (self.db.encode_key(key),))[0]

    def test_int(self):
        self.db['test'] = -42
        assert self.db['test'] == -42
        assert self.get_json('test') == '-42'

    def test_str(self):
        test_str = u'Test \u30c6\u30b9\u30c8'
        self.db['test'] = test_str
        assert self.db['test'] == test_str
        assert self.get_json('test') == r'"Test \u30c6\u30b9\u30c8"'

    def test_bool(self):
        self.db['test'] = False
        assert self.db['test'] is False
        assert self.get_json('test') == 'false'

    def test_none(self):
        self.db['test'] = None
        assert self.db['test'] is None
        assert self.get_json('test') == 'null'

    def test_complex_struct(self):
        test_value = {
            'version': 2.5,
            'items': ['one', 'two'],
        }
        self.db['test'] = test_value
        assert self.db['test'] == test_value
        assert self.get_json('test') == json.dumps(test_value)


class TablenamesTest(unittest.TestCase):
    def tearDown(self):
        for f in ('tablenames-test-1.sqlite', 'tablenames-test-2.sqlite'):
            path = norm_file(os.path.join('tests/db', f))
            if os.path.isfile(path):
                os.unlink(path)

    def test_tablenames_unnamed(self):
        fname = norm_file('tests/db/tablenames-test-1.sqlite')
        SqliteDict(fname)
        self.assertEqual(SqliteDict.get_tablenames(fname), ['unnamed'])

    def test_tablenams_named(self):
        fname = norm_file('tests/db/tablenames-test-2.sqlite')
        with SqliteDict(fname, tablename='table1'):
            self.assertEqual(SqliteDict.get_tablenames(fname), ['table1'])
        with SqliteDict(fname, tablename='table2'):
            self.assertEqual(SqliteDict.get_tablenames(fname), ['table1', 'table2'])

        tablenames = SqliteDict.get_tablenames('tests/db/tablenames-test-2.sqlite')
        self.assertEqual(tablenames, ['table1', 'table2'])


class SqliteDictKeySerializationTest(unittest.TestCase):
    def setUp(self):
        self.fname = norm_file('tests/db-encode-key/sqlitedict.sqlite')
        self.db = SqliteDict(
            filename=self.fname, tablename='test',
            encode_key=sqlitedict.encode_key, decode_key=sqlitedict.decode_key,
        )

    def test_nonstr_keys(self):
        self.db['test'] = -42
        assert self.db['test'] == -42
        self.db[(0, 1, 2)] = 17
        assert self.db[(0, 1, 2)] == 17
