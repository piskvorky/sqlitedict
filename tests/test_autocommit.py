import sys, os

def test():
    "Verify autocommit just before program exits."
    assert(0 == os.system('%s tests/autocommit.py' % sys.executable))
    assert(0 == os.system('%s tests/autocommit2.py' % sys.executable))
