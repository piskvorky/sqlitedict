"""Commit failures must reach the caller without killing the database worker."""
import os
import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize('mode', ['blocking', 'nonblocking', 'automatic'])
def test_locked_commit_can_be_retried(tmp_path, mode):
    # Isolate the regression: an unhandled worker exception used to leave the
    # caller blocked forever. A subprocess timeout bounds that failure.
    code = textwrap.dedent('''\
        import sqlite3
        import sys
        import time
        from sqlitedict import SqliteDict

        filename, mode = sys.argv[1:]
        db = SqliteDict(filename, journal_mode='DELETE')
        worker = db.conn
        reader = sqlite3.connect(filename)
        try:
            worker.select_one('PRAGMA busy_timeout=20')
            db['pending'] = 'value'
            worker.select_one('SELECT 1')
            reader.execute('BEGIN')
            reader.execute('SELECT * FROM unnamed').fetchall()

            if mode == 'blocking':
                try:
                    db.commit()
                except sqlite3.OperationalError as error:
                    assert 'locked' in str(error)
                else:
                    raise AssertionError('commit must report the lock')
            else:
                if mode == 'nonblocking':
                    db.commit(blocking=False)
                else:
                    worker.autocommit = True
                    worker.execute('SELECT 1')
                deadline = time.monotonic() + 3
                while worker.is_alive() and time.monotonic() < deadline:
                    with worker._lock:
                        if worker.exception is not None:
                            break
                    time.sleep(0.001)
                try:
                    worker.check_raise_error()
                except sqlite3.OperationalError as error:
                    assert 'locked' in str(error)
                else:
                    raise AssertionError('commit error was lost')

            assert worker.is_alive()
            reader.rollback()
            db.commit()
            assert db['pending'] == 'value'
            db.close()
            assert not worker.is_alive()
            with SqliteDict(filename, flag='r') as reopened:
                assert reopened['pending'] == 'value'
        finally:
            reader.close()
            db.close(force=True)
    ''')
    result = subprocess.run(
        [sys.executable, '-c', code, str(tmp_path / 'locked.sqlite'), mode],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
        universal_newlines=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
