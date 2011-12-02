===============================================================
sqlitedict -- persistent `dict`, backed-up by SQLite and pickle
===============================================================

A lightweight wrapper around Python's sqlite3 database, with a dict-like interface
and multi-thread access support::

>>> mydict = SqliteDict('some.db', autocommit=True) # the mapping will be persisted to file `some.db`
>>> mydict['some_key'] = any_picklable_object
>>> print mydict['some_key']
>>> print len(mydict) # etc... all dict functions work

Pickle is used internally to serialize the values. Keys are strings.

If you don't use autocommit (default is no autocommit for performance), then
don't forget to call `mydict.commit()` when done with a transaction.

Features
--------

* Values can be **any picklable objects** (uses `cPickle` with the highest protocol).
* Support for **multiple tables** (=dicts) living in the same database file.
* Support for **access from multiple threads** to the same connection (needed by e.g. Pyro).
  Vanilla sqlite3 gives you `ProgrammingError: SQLite objects created in a thread can
  only be used in that same thread.`

Concurrent requests are still serialized internally, so this "multithreaded support"
**doesn't** give you any performance benefits. It is a work-around for sqlite limitations in Python.

Installation
------------

The module has no dependencies beyond 2.5 <= Python < 3.0. Install or upgrade with::

    sudo easy_install -U sqlitedict

or from the `source tar.gz <http://pypi.python.org/pypi/sqlitedict>`_ ::

    python sqlitedict.py # run some tests
    sudo python setup.py install

Documentation
-------------

Standard Python document strings are inside the module::

>>> import sqlitedict
>>> help(sqlitedict)

(but it's just `dict` with a commit, really).

Comments, bug reports
---------------------

`sqlitedict` resides on `github <https://github.com/piskvorky/sqlitedict>`_. You can file
issues or pull requests there.

----

`sqlitedict` is released as public domain, you may do with it as you please. Hack away.
