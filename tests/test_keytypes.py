# encoding: utf-8
"""Ensure different types of key, including mutable and immutable, works"""

# std imports
import unittest

# local
import sqlitedict

class KeyTypeTest(unittest.TestCase):
    def test_list_key(self):
        """Use list object as key"""
        fname = 'tests/db/sqlitedict-mutable-test.sqlite'
        d = sqlitedict2.SqliteDict(fname, autocommit=True)
        k1 = [1,2]
        k2 = k1.copy()
        d[k1] = 3
        self.assertEqual(d[k1], 3)
        self.assertEqual(d[k2], 3)
        k1.append('3')
        d[k1] = 4
        self.assertEqual(d[k1], 4)
        self.assertEqual(d[k2], 3)
        
    def test_float_tuple_key(self):
        """Use float tuple object as key
        
        k1 == k2 but k1 is not k2
        """
        fname = 'tests/db/sqlitedict2-mutable-test.sqlite'
        d = sqlitedict.SqliteDict(fname, autocommit=True)
        k1 = (1.1, 2.2)
        k2 = (1.1, 2.2)
        self.assertIsNot(k1, k2)
        d[k1] = 3
        self.assertEqual(d[k1], 3)
        self.assertEqual(d[k2], 3)
        d[k2] = 4
        self.assertEqual(d[k1], 4)
        self.assertEqual(d[k2], 4)
