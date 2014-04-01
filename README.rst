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

**Beware**: because of Python semantics, `sqlitedict` cannot know when a mutable persistent-dictionary entry was modified.
For example, `mydict.setdefault('new_key', []).append(1)` will leave `mydict['new_key']` equal to empty list, not `[1]`.
You'll need to explicitly assign the mutated object back to achieve the same effect::

>>> val = mydict.get('new_key', [])
>>> val.append(1)
>>> mydict['new_key'] = val


**Note**: due to the way the keys are handled internally, mydict[5] and mydict['5'] both refer to the single key '5'::

>>> mydict = sqlitedict.SqliteDict()
>>> mydict[9] = 'town'
>>> mydict['4'] = 'zebra'
>>> mydict.keys()
>>> # ['9', '4']
>>> mydict[4]
>>> # 'zebra'


Comments, bug reports
---------------------

`sqlitedict` resides on `github <https://github.com/piskvorky/sqlitedict>`_. You can file
issues or pull requests there.

----

`sqlitedict` is released as public domain, you may do with it as you please. Hack away.
