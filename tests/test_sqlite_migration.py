# encoding: utf-8
import unittest
import sqlite_migration
import sqlitedict

from accessories import norm_file, TestCaseBackport

from sys import version_info
_major_version = version_info[0]


class MigrationTest(TestCaseBackport):

    def setUp(self):
        self.file = norm_file('tests/db/migrate.sqlite')
        self.table_name = 'unnamed'
        MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value BLOB)' % self.table_name
        self.conn = sqlitedict.SqliteMultithread(self.file, autocommit=True, journal_mode="DELETE")
        self.conn.execute(MAKE_TABLE)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_migrate(self):
        # adding manually items with plain text keys
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn.execute(ADD_ITEM, ("abcd", sqlitedict.encode("abcd")))
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn.execute(ADD_ITEM, ("xyz", sqlitedict.encode(24)))
        # migrating the DB
        sqlite_migration.migrate(self.file, self.table_name, self.conn)
        # checking migrated DB via sqlitedict
        d = sqlitedict.SqliteDict(filename=self.file, tablename=self.table_name, autocommit=True)
        self.assertEqual(d["abcd"], "abcd")
        self.assertEqual(d["xyz"], 24)
        d.terminate()
