# encoding: utf-8
import unittest
import sqlitedict

from accessories import TestCaseBackport

from sys import version_info
_major_version=version_info[0]


class _ClassType(object):
    def __init__(self, value):
        self._value = value
    def __eq__(self, other):
        return self._value == other._value


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

        self.assertEqual(len(self.d), 0, self.d.items())
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

    def _assert_keyvalue(self, given_key, given_val):
        # given,
        with sqlitedict.SqliteDict() as db:
            # exercise
            db[given_key] = given_val
            result_key = db.keys()[0]
            #assert result_key == given_key, (result_key, given_key)
            #result_val = db[result_key]
            result_val = db[given_key]

        # verify
        assert type(result_key) == type(given_key), (result_key, given_key)
        assert type(result_val) == type(given_val), (result_val, given_val)
        assert result_key == given_key, (result_key, given_key)
        assert result_val == given_val, (result_val, given_val)

    def test_strtype(self):
        """Ensure key of type u'nicode'."""
        self._assert_keyvalue(b'some-key', b'some-val')

    def test_unicode(self):
        """Ensure key of type b'ytestring'."""
        self._assert_keyvalue(u'ǝpoɔıun', u'ǝpoɔıun')

    def test_tupletype(self):
        """Ensure key of type (tu, ple)."""
        self._assert_keyvalue((u'1', 2), (u'3', 4))

    def test_listtype(self):
        """Ensure key of type (li, st)."""
        self._assert_keyvalue([u'1', 2], [u'3', 4])

    def test_classtype(self):
        """Ensure key of class instance type."""
        key = _ClassType(u'some-key')
        val = _ClassType(u'some-val')
        self._assert_keyvalue(key, val)

    def test_dicttype(self):
        """Ensure keys may be pickled as type dict."""
        self._assert_keyvalue({u'ftp': 21, u'telnet': 23}, b'/etc/services')
