#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code is distributed under the terms and conditions
# from the Apache License, Version 2.0
#
# http://opensource.org/licenses/apache2.0.php
#
# This code was inspired by:
#  * http://code.activestate.com/recipes/576638-draft-for-an-sqlite3-based-dbm/
#  * http://code.activestate.com/recipes/526618/

"""
A lightweight wrapper around Python's sqlite3 database, with a dict-like interface
and multi-thread access support::

>>> mydict = SqliteDict('some.db', autocommit=True) # the mapping will be persisted to file `some.db`
>>> mydict['some_key'] = any_picklable_object
>>> print mydict['some_key']
>>> print len(mydict) # etc... all dict functions work

Pickle is used internally to serialize the values. Keys are strings.

If you don't use autocommit (default is no autocommit for performance), then
don't forget to call `mydict.commit()` when done with a transaction.

"""

import sqlite3
import os
import sys
import tempfile
import random
import logging
import traceback

from threading import Thread

try:
    __version__ = __import__('pkg_resources').get_distribution('sqlitedict').version
except:
    __version__ = '?'

major_version = sys.version_info[0]
if major_version < 3:  # py <= 2.x
    if sys.version_info[1] < 5:  # py <= 2.4
        raise ImportError("sqlitedict requires python 2.5 or higher (python 3.3 or higher supported)")

    # necessary to use exec()_ as this would be a SyntaxError in python3.
    # this is an exact port of six.reraise():
    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("""exec _code_ in _globs_, _locs_""")

    exec_("def reraise(tp, value, tb=None):\n"
          "    raise tp, value, tb\n")
else:
    def reraise(tp, value, tb=None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

try:
    from cPickle import dumps, loads, HIGHEST_PROTOCOL as PICKLE_PROTOCOL
except ImportError:
    from pickle import dumps, loads, HIGHEST_PROTOCOL as PICKLE_PROTOCOL

# some Python 3 vs 2 imports
try:
    from collections import UserDict as DictClass
except ImportError:
    from UserDict import DictMixin as DictClass

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


logger = logging.getLogger(__name__)


def open(*args, **kwargs):
    """See documentation of the SqliteDict class."""
    return SqliteDict(*args, **kwargs)


def encode(obj):
    """Serialize an object using pickle to a binary format accepted by SQLite."""
    return sqlite3.Binary(dumps(obj, protocol=PICKLE_PROTOCOL))


def decode(obj):
    """Deserialize objects retrieved from SQLite."""
    return loads(bytes(obj))


class SqliteDict(DictClass):
    VALID_FLAGS = ['c', 'r', 'w', 'n']

    def __init__(self, filename=None, tablename='unnamed', flag='c',
                 autocommit=False, journal_mode="DELETE"):
        """
        Initialize a thread-safe sqlite-backed dictionary. The dictionary will
        be a table `tablename` in database file `filename`. A single file (=database)
        may contain multiple tables.

        If no `filename` is given, a random file in temp will be used (and deleted
        from temp once the dict is closed/deleted).

        If you enable `autocommit`, changes will be committed after each operation
        (more inefficient but safer). Otherwise, changes are committed on `self.commit()`,
        `self.clear()` and `self.close()`.

        Set `journal_mode` to 'OFF' if you're experiencing sqlite I/O problems
        or if you need performance and don't care about crash-consistency.

        The `flag` parameter. Exactly one of:
          'c': default mode, open for read/write, creating the db/table if necessary.
          'w': open for r/w, but drop `tablename` contents first (start with empty table)
          'r': open as read-only
          'n': create a new database (erasing any existing tables, not just `tablename`!).

        """
        self.in_temp = filename is None
        if self.in_temp:
            randpart = hex(random.randint(0, 0xffffff))[2:]
            filename = os.path.join(tempfile.gettempdir(), 'sqldict' + randpart)

        if flag not in SqliteDict.VALID_FLAGS:
            raise RuntimeError("Unrecognized flag: %s" % flag)
        self.flag = flag

        if flag == 'n':
            if os.path.exists(filename):
                os.remove(filename)

        dirname = os.path.dirname(filename)
        if dirname:
            if not os.path.exists(dirname):
                raise RuntimeError('Error! The directory does not exist, %s' % dirname)

        self.filename = filename
        self.tablename = tablename

        logger.info("opening Sqlite table %r in %s" % (tablename, filename))
        MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value BLOB)' % self.tablename
        self.conn = SqliteMultithread(filename, autocommit=autocommit, journal_mode=journal_mode)
        self.conn.execute(MAKE_TABLE)
        self.conn.commit()
        if flag == 'w':
            self.clear()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def __str__(self):
        return "SqliteDict(%s)" % (self.filename)

    def __repr__(self):
        return str(self)  # no need of something complex

    def __len__(self):
        # `select count (*)` is super slow in sqlite (does a linear scan!!)
        # As a result, len() is very slow too once the table size grows beyond trivial.
        # We could keep the total count of rows ourselves, by means of triggers,
        # but that seems too complicated and would slow down normal operation
        # (insert/delete etc).
        GET_LEN = 'SELECT COUNT(*) FROM %s' % self.tablename
        rows = self.conn.select_one(GET_LEN)[0]
        return rows if rows is not None else 0

    def __bool__(self):
        # No elements is False, otherwise True
        GET_MAX = 'SELECT MAX(ROWID) FROM %s' % self.tablename
        m = self.conn.select_one(GET_MAX)[0]
        # Explicit better than implicit and bla bla
        return True if m is not None else False

    def iterkeys(self):
        GET_KEYS = 'SELECT key FROM %s ORDER BY rowid' % self.tablename
        for key in self.conn.select(GET_KEYS):
            yield key[0]

    def itervalues(self):
        GET_VALUES = 'SELECT value FROM %s ORDER BY rowid' % self.tablename
        for value in self.conn.select(GET_VALUES):
            yield decode(value[0])

    def iteritems(self):
        GET_ITEMS = 'SELECT key, value FROM %s ORDER BY rowid' % self.tablename
        for key, value in self.conn.select(GET_ITEMS):
            yield key, decode(value)

    def keys(self):
        return self.iterkeys() if major_version > 2 else list(self.iterkeys())

    def values(self):
        return self.itervalues() if major_version > 2 else list(self.itervalues())

    def items(self):
        return self.iteritems() if major_version > 2 else list(self.iteritems())

    def __contains__(self, key):
        HAS_ITEM = 'SELECT 1 FROM %s WHERE key = ?' % self.tablename
        return self.conn.select_one(HAS_ITEM, (key,)) is not None

    def __getitem__(self, key):
        GET_ITEM = 'SELECT value FROM %s WHERE key = ?' % self.tablename
        item = self.conn.select_one(GET_ITEM, (key,))
        if item is None:
            raise KeyError(key)
        return decode(item[0])

    def __setitem__(self, key, value):
        if self.flag == 'r':
            raise RuntimeError('Refusing to write to read-only SqliteDict')

        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self.tablename
        self.conn.execute(ADD_ITEM, (key, encode(value)))

    def __delitem__(self, key):
        if self.flag == 'r':
            raise RuntimeError('Refusing to delete from read-only SqliteDict')

        if key not in self:
            raise KeyError(key)
        DEL_ITEM = 'DELETE FROM %s WHERE key = ?' % self.tablename
        self.conn.execute(DEL_ITEM, (key,))

    def update(self, items=(), **kwds):
        if self.flag == 'r':
            raise RuntimeError('Refusing to update read-only SqliteDict')

        try:
            items = items.items()
        except AttributeError:
            pass
        items = [(k, encode(v)) for k, v in items]

        UPDATE_ITEMS = 'REPLACE INTO %s (key, value) VALUES (?, ?)' % self.tablename
        self.conn.executemany(UPDATE_ITEMS, items)
        if kwds:
            self.update(kwds)

    def __iter__(self):
        return self.iterkeys()

    def clear(self):
        if self.flag == 'r':
            raise RuntimeError('Refusing to clear read-only SqliteDict')

        CLEAR_ALL = 'DELETE FROM %s;' % self.tablename  # avoid VACUUM, as it gives "OperationalError: database schema has changed"
        self.conn.commit()
        self.conn.execute(CLEAR_ALL)
        self.conn.commit()

    def commit(self, blocking=True):
        """
        Persist all data to disk.

        When `blocking` is False, the commit command is queued, but the data is
        not guaranteed persisted (default implication when autocommit=True).
        """
        if self.conn is not None:
            self.conn.commit(blocking)
    sync = commit

    def close(self, do_log=True):
        if do_log:
            logger.debug("closing %s" % self)
        if hasattr(self, 'conn') and self.conn is not None:
            if self.conn.autocommit:
                # typically calls to commit are non-blocking when autocommit is
                # used.  However, we need to block on close() to ensure any
                # awaiting exceptions are handled and that all data is
                # persisted to disk before returning.
                self.conn.commit(blocking=True)
            self.conn.close()
            self.conn = None
        if self.in_temp:
            try:
                os.remove(self.filename)
            except:
                pass

    def terminate(self):
        """Delete the underlying database file. Use with care."""
        if self.flag == 'r':
            raise RuntimeError('Refusing to terminate read-only SqliteDict')

        self.close()

        if self.filename == ':memory:':
            return

        logger.info("deleting %s" % self.filename)
        try:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
        except (OSError, IOError):
            logger.exception("failed to delete %s" % (self.filename))

    def __del__(self):
        # like close(), but assume globals are gone by now (do not log!)
        try:
            self.close(do_log=False)
        except Exception:
            # prevent error log flood in case of multiple SqliteDicts
            # closed after connection lost (exceptions are always ignored
            # in __del__ method.
            pass

# Adding extra methods for python 2 compatibility (at import time)
if major_version == 2:
    SqliteDict.__nonzero__ = SqliteDict.__bool__
    del SqliteDict.__bool__  # not needed and confusing
#endclass SqliteDict


class SqliteMultithread(Thread):
    """
    Wrap sqlite connection in a way that allows concurrent requests from multiple threads.

    This is done by internally queueing the requests and processing them sequentially
    in a separate thread (in the same order they arrived).

    """
    def __init__(self, filename, autocommit, journal_mode):
        super(SqliteMultithread, self).__init__()
        self.filename = filename
        self.autocommit = autocommit
        self.journal_mode = journal_mode
        # use request queue of unlimited size
        self.reqs = Queue()
        self.setDaemon(True)  # python2.5-compatible
        self.exception = None
        self.log = logging.getLogger('sqlitedict.SqliteMultithread')
        self.start()

    def run(self):
        if self.autocommit:
            conn = sqlite3.connect(self.filename, isolation_level=None, check_same_thread=False)
        else:
            conn = sqlite3.connect(self.filename, check_same_thread=False)
        conn.execute('PRAGMA journal_mode = %s' % self.journal_mode)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('PRAGMA synchronous=OFF')

        res = None
        while True:
            req, arg, res, outer_stack = self.reqs.get()
            if req == '--close--':
                assert res, ('--close-- without return queue', res)
                break
            elif req == '--commit--':
                conn.commit()
                if res:
                    res.put('--no more--')
            else:
                try:
                    cursor.execute(req, arg)
                except Exception as err:
                    self.exception = (e_type, e_value, e_tb) = sys.exc_info()
                    inner_stack = traceback.extract_stack()

                    # An exception occurred in our thread, but we may not
                    # immediately able to throw it in our calling thread, if it has
                    # no return `res` queue: log as level ERROR both the inner and
                    # outer exception immediately.
                    #
                    # Any iteration of res.get() or any next call will detect the
                    # inner exception and re-raise it in the calling Thread; though
                    # it may be confusing to see an exception for an unrelated
                    # statement, an ERROR log statement from the 'sqlitedict.*'
                    # namespace contains the original outer stack location.
                    self.log.error('Inner exception:')
                    for item in traceback.format_list(inner_stack):
                        self.log.error(item)
                    self.log.error('')  # deliniate traceback & exception w/blank line
                    for item in traceback.format_exception_only(e_type, e_value):
                        self.log.error(item)

                    self.log.error('')  # exception & outer stack w/blank line
                    self.log.error('Outer stack:')
                    for item in traceback.format_list(outer_stack):
                        self.log.error(item)
                    self.log.error('Exception will be re-raised at next call.')

                if res:
                    for rec in cursor:
                        res.put(rec)
                    res.put('--no more--')

                if self.autocommit:
                    conn.commit()

        self.log.debug('received: %s, send: --no more--', req)
        conn.close()
        res.put('--no more--')

    def check_raise_error(self):
        """
        Check for and raise exception for any previous sqlite query.

        For the `execute*` family of method calls, such calls are non-blocking and any
        exception raised in the thread cannot be handled by the calling Thread (usually
        MainThread).  This method is called on `close`, and prior to any subsequent
        calls to the `execute*` methods to check for and raise an exception in a
        previous call to the MainThread.
        """
        if self.exception:
            e_type, e_value, e_tb = self.exception

            # clear self.exception, if the caller decides to handle such
            # exception, we should not repeatedly re-raise it.
            self.exception = None

            self.log.error('An exception occurred from a previous statement, view '
                           'the logging namespace "sqlitedict" for outer stack.')

            # The third argument to raise is the traceback object, and it is
            # substituted instead of the current location as the place where
            # the exception occurred, this is so that when using debuggers such
            # as `pdb', or simply evaluating the naturally raised traceback, we
            # retain the original (inner) location of where the exception
            # occurred.
            reraise(e_type, e_value, e_tb)

    def execute(self, req, arg=None, res=None):
        """
        `execute` calls are non-blocking: just queue up the request and return immediately.
        """
        self.check_raise_error()

        # NOTE: This might be a lot of information to pump into an input
        # queue, affecting performance.  I've also seen earlier versions of
        # jython take a severe performance impact for throwing exceptions
        # so often.
        stack = traceback.extract_stack()[:-1]
        self.reqs.put((req, arg or tuple(), res, stack))

    def executemany(self, req, items):
        for item in items:
            self.execute(req, item)
        self.check_raise_error()

    def select(self, req, arg=None):
        """
        Unlike sqlite's native select, this select doesn't handle iteration efficiently.

        The result of `select` starts filling up with values as soon as the
        request is dequeued, and although you can iterate over the result normally
        (`for res in self.select(): ...`), the entire result will be in memory.
        """
        res = Queue()  # results of the select will appear as items in this queue
        self.execute(req, arg, res)
        while True:
            rec = res.get()
            self.check_raise_error()
            if rec == '--no more--':
                break
            yield rec

    def select_one(self, req, arg=None):
        """Return only the first row of the SELECT, or None if there are no matching rows."""
        try:
            return next(iter(self.select(req, arg)))
        except StopIteration:
            return None

    def commit(self, blocking=True):
        if blocking:
            # by default, we await completion of commit() unless
            # blocking=False.  This ensures any available exceptions for any
            # previous statement are thrown before returning, and that the
            # data has actually persisted to disk!
            self.select_one('--commit--')
        else:
            # otherwise, we fire and forget as usual.
            self.execute('--commit--')

    def close(self):
        # we abuse 'select' to "iter" over a "--close--" statement so that we
        # can confirm the completion of close before joining the thread and
        # returning (by semaphore '--no more--'
        self.select_one('--close--')
        self.join()
#endclass SqliteMultithread
