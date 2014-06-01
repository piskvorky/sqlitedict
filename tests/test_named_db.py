import os
import sqlitedict

from test_temp_db import TempSqliteDictTest


def norm_file(fname):
    """Normalize test filename, creating a directory path to it if necessary"""
    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return fname


class NamedSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-def.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db)


class CreateNewSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-n-flag.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, flag="n")

    def tearDown(self):
        self.d.terminate()


class StartsWithEmptySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-with-w-flag.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, flag="w")

    def tearDown(self):
        self.d.terminate()



class SqliteDictAutocommitTest(TempSqliteDictTest):

    def setUp(self):
        db = norm_file('tests/db/sqlitedict-autocommit.sqlite')
        self.d = sqlitedict.SqliteDict(filename=db, autocommit=True)

    def tearDown(self):
        self.d.terminate()
