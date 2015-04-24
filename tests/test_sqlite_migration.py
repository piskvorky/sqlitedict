# encoding: utf-8
import sqlite_migration
import sqlitedict

from accessories import norm_file, TestCaseBackport

from sys import version_info
_major_version = version_info[0]


class MigrationTest(TestCaseBackport):

    def setUp(self):
        self.old_file = norm_file('./test/db/migrate.sqlite')
        self.new_file = norm_file('./test/db/migrate_new.sqlite')
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

    def test_migrate(self):
        # adding manually items with plain text keys
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, ("abcd", sqlitedict.encode("abcd")))
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, ("xyz", sqlitedict.encode(24)))
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.table_name
        self.conn_old.execute(ADD_ITEM, ("+ěščřžýáíé%123456789úů", sqlitedict.encode("special")))
        # migrating the DB
        sqlite_migration.migrate(self.table_name, self.conn_old, self.conn_new)
        # checking migrated DB via sqlitedict
        d = sqlitedict.SqliteDict(filename=self.new_file, tablename=self.table_name, autocommit=True)
        self.assertEqual(d["abcd"], "abcd")
        self.assertEqual(d["xyz"], 24)
        self.assertEqual(d["+ěščřžýáíé%123456789úů"], "special")
        d.terminate()
