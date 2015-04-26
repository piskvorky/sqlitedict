# encoding: utf-8
# std imports
import os

# local
import sqlite_migration
import sqlitedict
from accessories import norm_file

# 3rd party
import unittest2


class MigrationTest(unittest2.TestCase):

    def setUp(self):
        self.old_file = norm_file(
            os.path.join(os.path.dirname(__file__),
                         'db', 'migrate.sqlite'))
        self.new_file = norm_file(
            os.path.join(os.path.dirname(__file__),
                         'db', 'migrate_new.sqlite'))
        self.table_name = 'unnamed'
        MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value BLOB)' % self.table_name
        self.conn_old = sqlitedict.SqliteMultithread(self.old_file, autocommit=True, journal_mode="DELETE")
        self.conn_old.execute(MAKE_TABLE)
        self.conn_old.commit()
        self.conn_new = sqlitedict.SqliteMultithread(self.new_file, autocommit=True, journal_mode="DELETE")
        self.conn_new.execute(MAKE_TABLE)
        self.conn_new.commit()

    def tearDown(self):
        self.conn_old.close()
        self.conn_new.close
        os.unlink(self.old_file)

    def test_migrate(self):
        # adding manually items with plain text keys
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, (b"abcd", sqlitedict.encode("abcd")))
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, (b"xyz", sqlitedict.encode(24)))
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, (b"+ěščřžýáíé%123456789úů", sqlitedict.encode("special")))
        # migrating the DB
        sqlite_migration.migrate(self.table_name, self.conn_old, self.conn_new)
        # checking migrated DB via sqlitedict
        d = sqlitedict.SqliteDict(filename=self.new_file, tablename=self.table_name, autocommit=True)
        self.assertEqual(d["abcd"], "abcd")
        self.assertEqual(d["xyz"], 24)
        self.assertEqual(d["+ěščřžýáíé%123456789úů"], "special")
        d.terminate()


class KeyErrorMigratedTest(unittest2.TestCase):
    def setUp(self):
        # create database of v1.2 values
        self.filename = norm_file(
            os.path.join(os.path.dirname(__file__),
                         'db', 'unmigrated.sqlite'))
        self.db = sqlitedict.SqliteDict(filename=self.filename, flag='n')
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.db.tablename
        keyval = (b"bytes", sqlitedict.encode(('some', 'value')))
        self.db.conn.execute(ADD_ITEM, keyval)

    def tearDown(self):
        self.db.close()
        self.db.terminate()

    def fail_unpickling_test(self):
        """On retrieval of any key, we fail unpickle."""
        with self.assertRaisesRegexp(KeyError, "your sqlite db is not compatible.*"):
            self.db.keys()
#            self.db[self.db.keys()[0]]
