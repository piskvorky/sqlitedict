import os
import unittest
import sqlitedict

class SqliteDictUtilsTest(unittest.TestCase):

    def test_terminate_instead_close(self):
        ''' make terminate() instead of close()
        '''
        d = sqlitedict.open('tests/db/sqlitedict-terminate.sqlite')
        d['abc'] = 'def'
        d.commit()
        self.assertEqual(d['abc'], 'def')
        d.terminate()
        self.assertFalse(os.path.isfile('tests/db/sqlitedict-terminate.sqlite'))

    def test_with_statement(self):
        ''' test_with_statement
        '''
        with sqlitedict.SqliteDict() as d:
            self.assertTrue(isinstance(d, sqlitedict.SqliteDict))
            self.assertEqual(dict(d), {})
            self.assertEqual(list(d), [])
            self.assertEqual(len(d), 0)
