import unittest
import sqlitedict

from test_temp_db import TempSqliteDictTest

class NamedSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict('tests/db/sqlitedict-with-def.sqlite')

    def tearDown(self):
        self.d.terminate()


class CreateNewSqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(
                        'tests/db/sqlitedict-with-n-flag.sqlite', 
                        flag="n")

    def tearDown(self):
        ''' first attempt of running test will not passed, because file
            will no be created. The next of tests will be passed as
            file tests/db/sqlitedict-with-n-flag.sqlite is exist
        '''
        pass


class StartsWithEmptySqliteDictTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.SqliteDict(
                        'tests/db/sqlitedict-with-w-flag.sqlite', 
                        flag="w")

    def tearDown(self):
        self.d.terminate()

