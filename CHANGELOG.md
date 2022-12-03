# Changes

## 2.1.0, 2022-12-03

- Introduced weak references (PR [#165](https://github.com/RaRe-Technologies/sqlitedict/pull/165), [@mpenkov](https://github.com/mpenkov))
- Properly handled race condition (PR [#164](https://github.com/RaRe-Technologies/sqlitedict/pull/164), [@mpenkov](https://github.com/mpenkov))
- Added optional (not enabled by default) ability to encode keys (PR [#161](https://github.com/RaRe-Technologies/sqlitedict/pull/161), [@rdyro](https://github.com/rdyro))
- Changed logging from info to debug (PR [#163](https://github.com/RaRe-Technologies/sqlitedict/pull/163), [@nvllsvm](https://github.com/nvllsvm))
- Updated supported versions in readme (PR [#158](https://github.com/RaRe-Technologies/sqlitedict/pull/158), [@plague006](https://github.com/plague006))
- Corrected spelling mistakes (PR [#166](https://github.com/RaRe-Technologies/sqlitedict/pull/166), [@EdwardBetts](https://github.com/EdwardBetts))

## 2.0.0, 2022-03-04

This release supports Python 3.7 and above.
If you need support for older versions, please use the previous release, 1.7.0.

- Do not create tables when in read-only mode (PR [#128](https://github.com/RaRe-Technologies/sqlitedict/pull/128), [@hholst80](https://github.com/hholst80))
- Use tempfile.mkstemp for safer temp file creation (PR [#106](https://github.com/RaRe-Technologies/sqlitedict/pull/106), [@ergoithz](https://github.com/ergoithz))
- Fix deadlock where opening database fails  (PR [#107](https://github.com/RaRe-Technologies/sqlitedict/pull/107), [@padelt](https://github.com/padelt))
- Make outer_stack a parameter (PR [#148](https://github.com/RaRe-Technologies/sqlitedict/pull/148), [@mpenkov](https://github.com/padelt))

## 1.7.0, 2018-09-04

* Add a blocking commit after each modification if autocommit is enabled. (PR [#94](https://github.com/RaRe-Technologies/sqlitedict/pull/94), [@endlisnis](https://github.com/endlisnis))
* Clean up license file names (PR [#99](https://github.com/RaRe-Technologies/sqlitedict/pull/99), [@r-barnes](https://github.com/r-barnes))
* support double quotes in table names (PR [#113](https://github.com/RaRe-Technologies/sqlitedict/pull/113), [@vcalv](https://github.com/vcalv))

## 1.6.0, 2018-09-18

* Add Add `get_tablenames` method (@transfluxus, #72)
* Add license files to dist (@toddrme2178, #79)
* Replace `easy_install` -> `pip` in README (@thechief389, #77)
* Update build badge (@menshikh-iv)

## 1.5.0, 2017-02-13

* Add encode and decode parameters to store json, compressed or pickled objects (@erosennin, #65)
* Python 3.6 fix: commit before turning off synchronous (@bit, #59)
* Update sqlite version to 3.8.2 (@tmylk, #63)

## 1.4.2, 2016-08-26

* Fix some hangs on closing. Let __enter__ re-open a closed connection. (@ecederstrand, #55)
* Surround table names with quotes. (@Digenis, #50)

## 1.4.1, 2016-05-15

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
