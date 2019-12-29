import sqlitedict
from test_temp_db import TempSqliteDictTest
from accessories import norm_file


class InMemorySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(filename=':memory:', autocommit=True)

    def tearDown(self):
        self.d.terminate()


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
