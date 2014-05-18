import unittest
import sqlitedict

class SqliteDictUtilsTest(unittest.TestCase):
    

    def test_terminate_instead_close(self):
        ''' make terminate() instead of close()
        '''
        self.d = sqlitedict.open('tests/db/sqlitedict-terminate.sqlite')
        self.d.commit()
        self.d.terminate()   

    def test_with_statement(self):
        ''' test_with_statement
        '''
        with sqlitedict.SqliteDict() as d:
            self.assertIs(type(d), sqlitedict.SqliteDict)
            self.assertEqual(dict(d), {})
            self.assertEqual(list(d), [])
            self.assertEqual(len(d), 0)

