import sys, os

def test():
    "Verify autocommit just before program exits."
    assert(0 == os.system('PYTHONPATH=. %s tests/autocommit.py' % sys.executable))
    # The above script relies on the autocommit feature working correctly.
    # Now, let's check if it actually worked.
    import sqlitedict
    d = sqlitedict.SqliteDict('tests/db/autocommit.sqlite')
    expected = {str(i): i for i in range(1000)}
    actual = {key: value for (key, value) in d.items()}
    assert expected == actual, [expected, actual]
