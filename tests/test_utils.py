import unittest
import sqlitedict

from test_temp_db import TempSqliteDictTest

class SqliteDictUtilsTest(TempSqliteDictTest):

    def setUp(self):
        self.d = sqlitedict.open('tests/db/sqlitedict-open.sqlite')

    def tearDown(self):
        self.d.terminate()   


class SqliteDictWithStatementTest(unittest.TestCase):

    def test_with_statement(self):
        ''' test_with_statement
        '''
        with sqlitedict.SqliteDict() as d:
            self.assertIs(type(d), sqlitedict.SqliteDict)
            self.assertEqual(dict(d), {})
            self.assertEqual(list(d), [])
            self.assertEqual(len(d), 0)

