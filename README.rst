===================================================
sqlitedict -- persistent ``dict``, backed by SQLite
===================================================

|GithubActions|_
|License|_

.. |GithubActions| image:: https://github.com/RaRe-Technologies/sqlitedict/actions/workflows/python-package.yml/badge.svg
.. |Downloads| image:: https://img.shields.io/pypi/dm/sqlitedict.svg
.. |License| image:: https://img.shields.io/pypi/l/sqlitedict.svg
.. _GithubActions: https://github.com/RaRe-Technologies/sqlitedict/actions/workflows/python-package.yml
.. _Downloads: https://pypi.python.org/pypi/sqlitedict
.. _License: https://pypi.python.org/pypi/sqlitedict

A lightweight wrapper around Python's sqlite3 database with a simple, Pythonic
dict-like interface and support for multi-thread access:

Usage
=====

Write
-----

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>> db = SqliteDict("example.sqlite")
    >>>
    >>> db["1"] = {"name": "first item"}
    >>> db["2"] = {"name": "second item"}
    >>> db["3"] = {"name": "yet another item"}
    >>>
    >>> # Commit to save the objects.
    >>> db.commit()
    >>>
    >>> db["4"] = {"name": "yet another item"}
    >>> # Oops, forgot to commit here, that object will never be saved.
    >>> # Always remember to commit, or enable autocommit with SqliteDict("example.sqlite", autocommit=True)
    >>> # Autocommit is off by default for performance.
    >>>
    >>> db.close()

Read
----

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>> db = SqliteDict("example.sqlite")
    >>>
    >>> print("There are %d items in the database" % len(db))
    There are 3 items in the database
    >>>
    >>> # Standard dict interface. items() values() keys() etc...
    >>> for key, item in db.items():
    ...     print("%s=%s" % (key, item))
    1={'name': 'first item'}
    2={'name': 'second item'}
    3={'name': 'yet another item'}
    >>>
    >>> db.close()

Efficiency
----------

By default, sqlitedict's exception handling favors verbosity over efficiency.
It extracts and outputs the outer exception stack to the error logs.
If you favor efficiency, then initialize the DB with outer_stack=False.

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>> db = SqliteDict("example.sqlite", outer_stack=False)  # True is the default
    >>> db[1]
    {'name': 'first item'}

Context Manager
---------------

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>>
    >>> # The database is automatically closed when leaving the with section.
    >>> # Uncommitted objects are not saved on close. REMEMBER TO COMMIT!
    >>>
    >>> with SqliteDict("example.sqlite") as db:
    ...     print("There are %d items in the database" % len(db))
    There are 3 items in the database

Tables
------

A database file can store multiple tables.
A default table is used when no table name is specified.

Note: Writes are serialized, having multiple tables does not improve performance.

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>>
    >>> products = SqliteDict("example.sqlite", tablename="product", autocommit=True)
    >>> manufacturers = SqliteDict("example.sqlite", tablename="manufacturer", autocommit=True)
    >>>
    >>> products["1"] = {"name": "first item",  "manufacturer_id": "1"}
    >>> products["2"] = {"name": "second item", "manufacturer_id": "1"}
    >>>
    >>> manufacturers["1"] = {"manufacturer_name": "afactory", "location": "US"}
    >>> manufacturers["2"] = {"manufacturer_name": "anotherfactory", "location": "UK"}
    >>>
    >>> tables = products.get_tablenames('example.sqlite')
    >>> print(tables)
    ['unnamed', 'product', 'manufacturer']
    >>>
    >>> products.close()
    >>> manufacturers.close()

In case you're wondering, the unnamed table comes from the previous examples,
where we did not specify a table name.

Serialization
-------------

Keys are strings. Values are any serializeable object.

By default Pickle is used internally to (de)serialize the values.

It's possible to use a custom (de)serializer, notably for JSON and for compression.

.. code-block:: python

    >>> # Use JSON instead of pickle
    >>> import json
    >>> with SqliteDict("example.sqlite", encode=json.dumps, decode=json.loads) as mydict:
    ...     pass
    >>>
    >>> # Apply zlib compression after pickling
    >>> import zlib, pickle, sqlite3
    >>>
    >>> def my_encode(obj):
    ...     return sqlite3.Binary(zlib.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)))
    >>>
    >>> def my_decode(obj):
    ...     return pickle.loads(zlib.decompress(bytes(obj)))
    >>>
    >>> with SqliteDict("example.sqlite", encode=my_encode, decode=my_decode) as mydict:
    ...     pass

It's also possible to use a custom (de)serializer for keys to allow non-string keys.

.. code-block:: python

    >>> # Use key encoding instead of default string keys only
    >>> from sqlitedict import encode_key, decode_key
    >>> with SqliteDict("example.sqlite", encode_key=encode_key, decode_key=decode_key) as mydict:
    ...     pass

More
----

Functions are well documented, see docstrings directly in ``sqlitedict.py`` or call ``help(sqlitedict)``.

**Beware**: because of Python semantics, ``sqlitedict`` cannot know when a mutable
SqliteDict-backed entry was modified in RAM. You'll need to
explicitly assign the mutated object back to SqliteDict:

.. code-block:: python

    >>> from sqlitedict import SqliteDict
    >>> db = SqliteDict("example.sqlite")
    >>> db["colors"] = {"red": (255, 0, 0)}
    >>> db.commit()
    >>>
    >>> colors = db["colors"]
    >>> colors["blue"] = (0, 0, 255) # sqlite DB not updated here!
    >>> db["colors"] = colors  # now updated
    >>>
    >>> db.commit() # remember to commit (or set autocommit)
    >>> db.close()

Features
========

* Values can be **any picklable objects** (uses ``pickle`` with the highest protocol).
* Support for **multiple tables** (=dicts) living in the same database file.
* Support for **access from multiple threads** to the same connection (needed by e.g. Pyro).
  Vanilla sqlite3 gives you ``ProgrammingError: SQLite objects created in a thread can
  only be used in that same thread.``

  Concurrent requests are still serialized internally, so this "multithreaded support"
  **doesn't** give you any performance benefits. It is a work-around for sqlite limitations in Python.

* Support for **custom serialization or compression**:

.. code-block:: python

  # use JSON instead of pickle
  >>> import json
  >>> mydict = SqliteDict('./my_db.sqlite', encode=json.dumps, decode=json.loads)

  # apply zlib compression after pickling
  >>> import zlib, pickle, sqlite3
  >>> def my_encode(obj):
  ...     return sqlite3.Binary(zlib.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)))
  >>> def my_decode(obj):
  ...     return pickle.loads(zlib.decompress(bytes(obj)))
  >>> mydict = SqliteDict('./my_db.sqlite', encode=my_encode, decode=my_decode)

* sqlite is efficient and can work effectively with large databases (multi gigabytes), not limited by memory.
* sqlitedict is mostly a thin wrapper around sqlite.
* ``items()`` ``keys()`` ``values()`` are iterating one by one, the rows are loaded in a worker thread and queued in memory.
* ``len()`` is calling sqlite to count rows, that is scanning the whole table.
* For better performance, write objects in batch and ``commit()`` once.

Installation
============

The module has no dependencies beyond Python itself.
The minimum supported Python version is 3.7, continuously tested on Python 3.7, 3.8, 3.9, and 3.10 `on Travis <https://travis-ci.org/RaRe-Technologies/sqlitedict>`_.

Install or upgrade with::

    pip install -U sqlitedict

or from the `source tar.gz <http://pypi.python.org/pypi/sqlitedict>`_::

    python setup.py install

Contributions
=============

Testing
-------

Install::

    $ pip install pytest coverage pytest-coverage

To perform all tests::

    $ mkdir -p tests/db
    $ pytest tests
    $ python -m doctest README.rst

To perform all tests with coverage::

    $ pytest tests --cov=sqlitedict

Comments, bug reports
---------------------

``sqlitedict`` resides on `github <https://github.com/RaRe-Technologies/sqlitedict>`_. You can file
issues or pull requests there.

License
=======

``sqlitedict`` is open source software released under the `Apache 2.0 license <http://opensource.org/licenses/apache2.0.php>`_.
Copyright (c) 2011-now `Radim Řehůřek <http://radimrehurek.com>`_ and contributors.

Housekeeping
============

Clean up the test database to keep each doctest run idempotent:

.. code-block:: python

   >>> import os
   >>> if __name__ == '__main__':
   ...     os.unlink('example.sqlite')
