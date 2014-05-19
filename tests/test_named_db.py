import unittest
import sqlitedict

from test_temp_db import TempSqliteDictTest

class NamedSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict('tests/db/sqlitedict-with-def.sqlite')

    def tearDown(self):
        self.d.terminate()


class CreateNewSqliteDictTest(TempSqliteDictTest):
    ''' first attempt of running test will not passed, because file
        is not created. The next of tests will be passed as
        file tests/db/sqlitedict-with-n-flag.sqlite is exist
    '''
    def setUp(self):
        self.d = sqlitedict.SqliteDict(
                        'tests/db/sqlitedict-with-n-flag.sqlite', 
                        flag="n")



class StartsWithEmptySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(
                        'tests/db/sqlitedict-with-w-flag.sqlite', 
                        flag="w")

    def tearDown(self):
        self.d.terminate()


class SqliteDictAutocommitTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(
                        'tests/db/sqlitedict-autocommit.sqlite', 
                        autocommit=True)

    def tearDown(self):
        self.d.terminate()
