# Disabled: requires mocking or digging into sqlite code to figure out how else
# we may be able to raise an InterfaceError.
#
#class test_nextquery_exception(TestCaseBackport):
#
#    def test_inner_exception(self):
#        """Validates that an exception is thrown on *next* query. """
#        # per issue #25 we currently expect this to fail, it happens
#        # to provide test coverage for the exception handling, however.
#        import sqlite3
#        # given,
#        given_key, given_val = (1, 2), (3, 4)
#        with sqlitedict.SqliteDict() as db:
#            # exercise
#            db[given_key] = given_val
#            with self.assertRaises(sqlite3.InterfaceError):
#                result_key = db.keys()[0]
