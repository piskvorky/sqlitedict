import sys, os

def test():
    "Verify autocommit just before program exits."
    assert os.system('PYTHONPATH=. %s tests/autocommit.py' % sys.executable) == 0
    # The above script relies on the autocommit feature working correctly.
    # Now, let's check if it actually worked.
    import sqlitedict
    d = sqlitedict.SqliteDict('tests/db/autocommit.sqlite')
    for i in range(1000):
        assert d[i] == i, "actual: %d expected: %d" % (d[i], i)
