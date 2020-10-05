======================================================================
sqlitedict -- persistent ``dict``, backed up by SQLite
======================================================================

|Travis|_
|License|_

.. |Travis| image:: https://travis-ci.org/RaRe-Technologies/sqlitedict.svg?branch=master
.. |Downloads| image:: https://img.shields.io/pypi/dm/sqlitedict.svg
.. |License| image:: https://img.shields.io/pypi/l/sqlitedict.svg
.. _Travis: https://travis-ci.org/RaRe-Technologies/sqlitedict
.. _Downloads: https://pypi.python.org/pypi/sqlitedict
.. _License: https://pypi.python.org/pypi/sqlitedict

A lightweight wrapper around Python's sqlite3 database with a simple, Pythonic
dict-like interface and support for multi-thread access:

Usage
=====

Write
-----

.. code-block:: python

    from sqlitedict import SqliteDict
    db = SqliteDict("./db.sqlite")

    db["1"] = {"name": "first item"}
    db["2"] = {"name": "second item"}
    db["3"] = {"name": "yet another item"}

    # Commit to save the objects.
    db.commit()

    db["4"] = {"name": "yet another item"}
    # Oops, forgot to commit here, that object will never be saved.

    # Always remember to commit, or enable autocommit with SqliteDict("./db.sqlite", autocommit=True)
    # Autocommit is off by default for performance.

Read
----

.. code-block:: python

    from sqlitedict import SqliteDict
    db = SqliteDict("./db.sqlite")

    print("There are {} items in the database".format(len(db)))

    # Standard dict interface. items() values() keys() etc...
    for key, item in db.items():
        print("{}={}".format(key, item))

Context Manager
---------------

.. code-block:: python

    from sqlitedict import SqliteDict

    # The database is automatically closed when leaving the with section.
    # Uncommited objects are not saved on close. REMEMBER TO COMMIT!

    with SqliteDict("./db.sqlite") as db:
        print("There are {} items in the database".format(len(db)))


Tables
------

A database file can store multiple tables.
A default table is used when no table name is specified.

Note: Writes are serialized, having multiple tables does not improve performance.

.. code-block:: python

    from sqlitedict import SqliteDict

    products = SqliteDict("./db.sqlite", tablename="product", autocommit=True)
    manufacturers = SqliteDict("./db.sqlite", tablename="manufacturer", autocommit=True)

    products["1"] = {"name": "first item",  "manufacturer_id": "1"}
    products["2"] = {"name": "second item", "manufacturer_id": "1"}

    manufacturers["1"] = {"manufacturer_name": "afactory", "location": "US"}
    manufacturers["2"] = {"manufacturer_name": "anotherfactory", "location": "UK"}

    tables = products.get_tablenames()
    print(tables)
    # ["product", "manufacturer"]

Serialization
-------------

Keys are strings. Values are any serializeable object.

By default Pickle is used internally to (de)serialize the values.

It's possible to use a custom (de)serializer, notably for JSON and for compression.

.. code-block:: python

    # Use JSON instead of pickle
    import json
    mydict = SqliteDict("./my_db.sqlite", encode=json.dumps, decode=json.loads)

    # Apply zlib compression after pickling
    import zlib, pickle, sqlite3

    def my_encode(obj):
        return sqlite3.Binary(zlib.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)))
    def my_decode(obj):
        return pickle.loads(zlib.decompress(bytes(obj)))

    mydict = SqliteDict("./my_db.sqlite", encode=my_encode, decode=my_decode)

More
----

Functions are well documented, see docstrings directly in ``sqlitedict.py`` or call ``help(sqlitedict)``.

**Beware**: because of Python semantics, ``sqlitedict`` cannot know when a mutable
SqliteDict-backed entry was modified in RAM. You'll need to
explicitly assign the mutated object back to SqliteDict:

.. code-block:: python

    item = db["123"]
    item["name"] = "hello world" # sqlite DB not updated here!
    db["123"] = val  # now updated

    db.commit() # remember to commit (or set autocommit)

Features
========

* Values can be **any picklable objects** (uses ``cPickle`` with the highest protocol).
* Support for **multiple tables** (=dicts) living in the same database file.
* Support for **access from multiple threads** to the same connection (needed by e.g. Pyro).
  Vanilla sqlite3 gives you ``ProgrammingError: SQLite objects created in a thread can
  only be used in that same thread.``

  Concurrent requests are still serialized internally, so this "multithreaded support"
  **doesn't** give you any performance benefits. It is a work-around for sqlite limitations in Python.

* Support for **custom serialization or compression**:

Performance
===========

* sqlite is efficient and can work effectively with large databases (multi gigabytes), not limited by memory.
* sqlitedict is mostly a thin wrapper around sqlite, conserving efficiency.
* ``items()`` ``keys()`` ``values()`` are iterating one by one, ``len()`` is calling sqlite to count rows.
* For better performance, write objects in batch and ``commit()`` once.
* When using pickle, make sure cPickle is installed (pip install cPickle).

Installation
============

The module has no dependencies beyond Python itself.
The minimum Python version is 2.6, continuously tested on Python 2.6, 2.7, 3.3, 3.4, 3.5, 3.6 `on Travis <https://travis-ci.org/RaRe-Technologies/sqlitedict>`_.

Install or upgrade with::

    pip install -U sqlitedict

or from the `source tar.gz <http://pypi.python.org/pypi/sqlitedict>`_::

    python setup.py install

Contributions
=============

Testing
-------

Install::

    # pip install nose
    # pip install coverage

To perform all tests::

   # make test-all

To perform all tests with coverage::

   # make test-all-with-coverage

Comments, bug reports
---------------------

``sqlitedict`` resides on `github <https://github.com/RaRe-Technologies/sqlitedict>`_. You can file
issues or pull requests there.

License
=======

``sqlitedict`` is open source software released under the `Apache 2.0 license <http://opensource.org/licenses/apache2.0.php>`_.
Copyright (c) 2011-now `Radim Řehůřek <http://radimrehurek.com>`_ and contributors.
