import os
import sys

import sqlitedict


def test():
    "Verify autocommit just before program exits."
    assert os.system('env PYTHONPATH=. %s tests/autocommit.py' % sys.executable) == 0
    # The above script relies on the autocommit feature working correctly.
    # Now, let's check if it actually worked.
    d = sqlitedict.SqliteDict('tests/db/autocommit.sqlite')
    for i in range(1000):
        assert d[i] == i, "actual: %s expected: %s" % (d[i], i)
