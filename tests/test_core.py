# std imports
import tempfile
import os

# local
import sqlitedict
from test_temp_db import TempSqliteDictTest
from accessories import norm_file

# 3rd party
import unittest2


class SqliteMiscTest(unittest2.TestCase):

    def test_with_statement(self):
        """Verify using sqlitedict as a contextmanager . """
        with sqlitedict.SqliteDict() as d:
            self.assertTrue(isinstance(d, sqlitedict.SqliteDict))
            self.assertEqual(dict(d), {})
            self.assertEqual(list(d), [])
            self.assertEqual(len(d), 0)

    def test_as_str(self):
        """Verify SqliteDict.__str__()."""
        # given,
        db = sqlitedict.SqliteDict()
        # exercise
        db.__str__()

    def test_as_repr(self):
        """Verify SqliteDict.__repr__()."""
        # given,
        db = sqlitedict.SqliteDict()
        # exercise
        db.__repr__()

    def test_directory_notfound(self):
        """Verify RuntimeError: directory does not exist."""
        # given: a non-existent directory,
        folder = tempfile.mkdtemp(prefix='sqlitedict-test')
        os.rmdir(folder)
        # exercise,
        with self.assertRaises(RuntimeError):
            sqlitedict.SqliteDict(filename=os.path.join(folder, 'nonexistent'))

    def test_commit_nonblocking(self):
        """Coverage for non-blocking commit."""
        # given,
        with sqlitedict.SqliteDict(autocommit=True) as d:
            # exercise: the implicit commit is nonblocking
            d['key'] = 'value'
            d.commit(blocking=False)


class NamedSqliteDictCreateOrReuseTest(TempSqliteDictTest):
    """Verify default flag='c', and flag='n' of SqliteDict()."""

    def test_default_reuse_existing_flag_c(self):
        """Re-opening of a database does not destroy it."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db = sqlitedict.SqliteDict(filename=fname)
        orig_db['key'] = 'value'
        orig_db.commit()
        orig_db.close()

        next_db = sqlitedict.SqliteDict(filename=fname)
        self.assertIn('key', next_db.keys())
        self.assertEqual(next_db['key'], 'value')

    def test_overwrite_using_flag_n(self):
        """Re-opening of a database with flag='c' destroys it all."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db = sqlitedict.SqliteDict(filename=fname, tablename='sometable')
        orig_db['key'] = 'value'
        orig_db.commit()
        orig_db.close()

        # verify,
        next_db = sqlitedict.SqliteDict(filename=fname, tablename='sometable', flag='n')
        self.assertNotIn('key', next_db.keys())


    def test_overwrite_using_flag_w(self):
        """Re-opening of a database with flag='w' destroys only the target table."""
        # given,
        fname = norm_file('tests/db/sqlitedict-override-test.sqlite')
        orig_db_1 = sqlitedict.SqliteDict(filename=fname, tablename='one')
        orig_db_1['key'] = 'value'
        orig_db_1.commit()
        orig_db_1.close()

        orig_db_2 = sqlitedict.SqliteDict(filename=fname, tablename='two')
        orig_db_2['key'] = 'value'
        orig_db_2.commit()
        orig_db_2.close()

        # verify, when re-opening table space 'one' with flag='2', we destroy
        # its contents.  However, when re-opening table space 'two' with
        # default flag='r', its contents remain.
        next_db_1 = sqlitedict.SqliteDict(filename=fname, tablename='one', flag='w')
        self.assertNotIn('key', next_db_1.keys())

        next_db_2 = sqlitedict.SqliteDict(filename=fname, tablename='two')
        self.assertIn('key', next_db_2.keys())

class SqliteDictTerminateTest(unittest2.TestCase):

    def test_terminate_instead_close(self):
        ''' make terminate() instead of close()
        '''
        d = sqlitedict.open('tests/db/sqlitedict-terminate.sqlite')
        d['abc'] = 'def'
        d.commit()
        self.assertEqual(d['abc'], 'def')
        d.terminate()
        self.assertFalse(os.path.isfile('tests/db/sqlitedict-terminate.sqlite'))

class SqliteDictTerminateFailTest(unittest2.TestCase):
    """Provide Coverage for SqliteDict.terminate()."""

    def setUp(self):
        self.fname = norm_file('tests/db-permdenied/sqlitedict.sqlite')
        self.db = sqlitedict.SqliteDict(filename=self.fname)
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
