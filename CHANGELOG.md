# Changes

## Unreleased

- Do not create tables when in read-only mode (PR [#128](https://github.com/RaRe-Technologies/sqlitedict/pull/128), [@hholst80](https://github.com/hholst80))

## 1.7.0, 04/09/2018

* Add a blocking commit after each modification if autocommit is enabled. (PR [#94](https://github.com/RaRe-Technologies/sqlitedict/pull/94), [@endlisnis](https://github.com/endlisnis))
* Clean up license file names (PR [#99](https://github.com/RaRe-Technologies/sqlitedict/pull/99), [@r-barnes](https://github.com/r-barnes))
* support double quotes in table names (PR [#113](https://github.com/RaRe-Technologies/sqlitedict/pull/113), [@vcalv](https://github.com/vcalv))

## 1.6.0, 18/09/2018

* Add Add `get_tablenames` method (@transfluxus, #72)
* Add license files to dist (@toddrme2178, #79)
* Replace `easy_install` -> `pip` in README (@thechief389, #77)
* Update build badge (@menshikh-iv)

## 1.5.0, 13/02/2017

* Add encode and decode parameters to store json, compressed or pickled objects (@erosennin, #65)
* Python 3.6 fix: commit before turning off synchronous (@bit, #59)
* Update sqlite version to 3.8.2 (@tmylk, #63)

## 1.4.2, 26/08/2016

* Fix some hangs on closing. Let __enter__ re-open a closed connection. (@ecederstrand, #55)
* Surround table names with quotes. (@Digenis, #50)

## 1.4.1, 15/05/2016

* Read-only mode (@nrhine1, #37)
* Check file exists before deleting (@adibo, #39)
* AttributeError after SqliteDict is closed (@guyskk, #40)
* Python 3.5 support (@jtatum, #47)
* Pickle when updating with 2-tuples seq (@Digenis, #49)
* Fix exit errors: TypeError("'NoneType' object is not callable",) (@janrygl, #45)

## 1.4.0

* fix regression where iterating over keys/values/items returned a full list instead of iterator

## 1.3.0

* improve error handling in multithreading (PR #28); 100% test coverage.

## 1.2.0

* full python 3 support, continuous testing via Travis CI.
