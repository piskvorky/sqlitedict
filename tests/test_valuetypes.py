import unittest
import sqlitedict

from accessories import TestCaseBackport

from sys import version_info
_major_version=version_info[0]

class TempSqliteDictTest(TestCaseBackport):

    def setUp(self):
        self.d = sqlitedict.SqliteDict()

    def tearDown(self):
        self.d.close()

    def test_create_sqlitedict(self):
        ''' test_create_sqlitedict
        '''
        self.assertIsInstance(self.d, sqlitedict.SqliteDict)
        self.assertEqual(dict(self.d), {})
        self.assertEqual(list(self.d), [])
        self.assertEqual(len(self.d), 0)

    def test_assign_values(self):
        ''' test_assign_values
        '''
        self.d[u'abc'] = u'edf'
        self.assertEqual(self.d[u'abc'], u'edf')
        self.assertEqual(len(self.d), 1)

    def test_clear_data(self):
        ''' test_clear_data
        '''
        self.d.update(a=1, b=2, c=3)
        self.assertEqual(len(self.d), 3)
        self.d.clear()
        self.assertEqual(len(self.d), 0)

    def test_manage_one_record(self):
        ''' test_manage_one_record
        '''
        self.d[u'abc'] = u'rsvp' * 100
        self.assertEqual(self.d[u'abc'], u'rsvp' * 100)
        self.d[u'abc'] = u'lmno'
        self.assertEqual(self.d[u'abc'], u'lmno')
        self.assertEqual(len(self.d), 1)
        del self.d[u'abc']
        self.assertEqual(len(self.d), 0)
        self.assertTrue(not self.d)

    def test_manage_few_records(self):
        ''' test_manage_few_records
        '''
        self.d[u'abc'] = u'lmno'
        self.d[u'xyz'] = u'pdq'
        self.assertEqual(len(self.d), 2)
        if _major_version == 2:
            self.assertEqual(list(self.d.iteritems()),
                            [(u'abc', u'lmno'), (u'xyz', u'pdq')])
        self.assertEqual(self.d.items(),
                        [(u'abc', u'lmno'), (u'xyz', u'pdq')])
        self.assertEqual(self.d.values(), [u'lmno', u'pdq'])
        self.assertEqual(self.d.keys(), [u'abc', u'xyz'])
        self.assertEqual(list(self.d), [u'abc', u'xyz'])

    def test_update_records(self):
        ''' test_update_records
        '''
        self.d.update(p=u'x', q=u'y', r=u'z')
        self.assertEqual(len(self.d), 3)
        # As far as I know dicts does not need to return
        # the elements in a specified order (sort() is required )
        self.assertEqual(sorted(self.d.items()),
                        sorted([(u'q', u'y'), (u'p', u'x'), (u'r', u'z')]))
        self.assertEqual(sorted(list(self.d)), sorted([u'q', u'p', u'r']))

    def test_handling_errors(self):
        ''' test_handling_errors
        '''
        def get_value(d, k):
            return d[k]

        def remove_nonexists(d, k):
            del d[k]

        with self.assertRaises(KeyError):
            remove_nonexists(self.d, u'abc')
        with self.assertRaises(KeyError):
            get_value(self.d, u'abc')
