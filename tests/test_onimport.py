"""Test cases for on-import logic."""
import unittest
import sys


class SqliteDict_cPickleImportTest(unittest.TestCase):
    """Verify fallback to 'pickle' module when 'cPickle' is not found."""
    def setUp(self):
        self.orig_meta_path = sys.meta_path
        self.orig_sqlitedict = sys.modules.pop('sqlitedict', None)

        class FauxMissingImport(object):
            def __init__(self, *args):
                self.module_names = args

            def find_module(self, fullname, path=None):
                if fullname in self.module_names:
                    return self
                return None

            def load_module(self, name):
                raise ImportError("No module named %s (FauxMissingImport)" % (name,))

        # ensure cPickle/pickle is not cached
        sys.modules.pop('cPickle', None)
        sys.modules.pop('pickle', None)

        # add our custom importer
        sys.meta_path.insert(0, FauxMissingImport('cPickle'))

    def tearDown(self):
        sys.meta_path = self.orig_meta_path
        if self.orig_sqlitedict:
            sys.modules['sqlitedict'] = self.orig_sqlitedict

    def test_cpickle_fallback_to_pickle(self):
        # exercise,
        sqlitedict = __import__("sqlitedict")
        # verify,
        self.assertIn('pickle', sys.modules.keys())
        self.assertIs(sqlitedict.dumps, sys.modules['pickle'].dumps)
