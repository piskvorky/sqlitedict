import sqlite3
import threading
import unittest

from sqlitedict import SqliteMultithread


class FailingRowWorker(SqliteMultithread):
    def _connect(self):
        conn, cursor = super()._connect()

        def checked(value):
            if value == 2:
                raise ValueError("bad second row")
            return value

        conn.create_function("checked", 1, checked)
        return conn, cursor


class FetchErrorTests(unittest.TestCase):
    def test_fetch_error_reaches_caller_and_worker_recovers(self):
        for autocommit in (False, True):
            with self.subTest(autocommit=autocommit):
                self._check_fetch_error(autocommit)

    def _check_fetch_error(self, autocommit):
        worker = FailingRowWorker(":memory:", autocommit, "DELETE")
        errors = []
        finished = threading.Event()

        def consume():
            try:
                list(worker.select("SELECT checked(column1) FROM (VALUES (1), (2))"))
            except Exception as exc:
                errors.append(exc)
            finally:
                finished.set()

        reader = threading.Thread(target=consume, daemon=True)
        try:
            reader.start()
            self.assertTrue(finished.wait(3), "query fetch error left the caller waiting")
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], sqlite3.OperationalError)
            self.assertIn("function", str(errors[0]))
            self.assertTrue(worker.is_alive())
            self.assertEqual(worker.select_one("SELECT 42"), (42,))
        finally:
            worker.close(force=True)
            worker.join(3)
            self.assertFalse(worker.is_alive())


if __name__ == "__main__":
    unittest.main()
