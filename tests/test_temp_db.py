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
        self.d['abc'] = 'edf'
        self.assertEqual(self.d['abc'], 'edf')
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
        self.d['abc'] = 'rsvp' * 100
        self.assertEqual(self.d['abc'], 'rsvp' * 100)
        self.d['abc'] = 'lmno'
        self.assertEqual(self.d['abc'], 'lmno')
        self.assertEqual(len(self.d), 1)
        del self.d['abc']
        self.assertEqual(len(self.d), 0)
        self.assertTrue(not self.d)

    def test_manage_few_records(self):
        ''' test_manage_few_records
        '''
        self.d['abc'] = 'lmno'
        self.d['xyz'] = 'pdq'
        self.assertEqual(len(self.d), 2)
        if _major_version == 2:
            self.assertEqual(list(self.d.iteritems()),
                            [('abc', 'lmno'), ('xyz', 'pdq')])
        self.assertEqual(self.d.items(),
                        [('abc', 'lmno'), ('xyz', 'pdq')])
        self.assertEqual(self.d.values(), ['lmno', 'pdq'])
        self.assertEqual(self.d.keys(), ['abc', 'xyz'])
        self.assertEqual(list(self.d), ['abc', 'xyz'])

    def test_records_with_picklable_key(self):
        ''' test_records_with_picklable_key
        '''
        self.d[["abc", "klm"]] = "xyz"
        self.d[("cde", "ftp")] = 35
        self.d[{"a": 3, "b": 6}] = "yse"
        self.assertEqual(len(self.d), 3)
        if _major_version == 2:
            self.assertEqual(list(self.d.iteritems()),
                            [(["abc", "klm"], "xyz"), (("cde", "ftp"), 35),
                             ({"a": 3, "b": 6}, "yse")])
        self.assertEqual(self.d.items(),
                        [(["abc", "klm"], "xyz"), (("cde", "ftp"), 35),
                             ({"a": 3, "b": 6}, "yse")])
        self.assertEqual(self.d.values(), ["xyz", 35, "yse"])
        self.assertEqual(self.d.keys(), [["abc", "klm"], ("cde", "ftp"), {"a": 3, "b": 6}])
        self.assertEqual(list(self.d), [["abc", "klm"], ("cde", "ftp"), {"a": 3, "b": 6}])

    def test_update_records(self):
        ''' test_update_records
        '''
        self.d.update(p='x', q='y', r='z')
        self.assertEqual(len(self.d), 3)
        # As far as I know dicts does not need to return
        # the elements in a specified order (sort() is required )
        self.assertEqual(sorted(self.d.items()),
                        sorted([('q', 'y'), ('p', 'x'), ('r', 'z')]))
        self.assertEqual(sorted(list(self.d)), sorted(['q', 'p', 'r']))

    def test_handling_errors(self):
        ''' test_handling_errors
        '''
        def get_value(d, k):
            return d[k]

        def remove_nonexists(d, k):
            del d[k]

        with self.assertRaises(KeyError):
            remove_nonexists(self.d, 'abc')
        with self.assertRaises(KeyError):
            get_value(self.d, 'abc')
