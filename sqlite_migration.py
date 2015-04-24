#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code is distributed under the terms and conditions
# from the Apache License, Version 2.0
#
# http://opensource.org/licenses/apache2.0.php

"""
USAGE: %(program)s sqlitedict_path tablename

This is the compatibility script to migrate the sqlite DB from version that is compatible with sqlitedict 1.x
to the version compatible with sqlitedict 2.x
"""
import logging
import os
import sys

from sqlitedict import encode, SqliteMultithread

logger = logging.getLogger(__name__)


def migrate(path, table_name, conn):
    # get all old keys
    GET_KEYS = 'SELECT key FROM %s ORDER BY rowid' % table_name
    old_keys = [key[0] for key in conn.select(GET_KEYS)]
    for key in list(old_keys):
        # get value for the given key
        GET_ITEM = 'SELECT value FROM %s WHERE key = ?' % table_name
        item = conn.select_one(GET_ITEM, (key,))
        # save record with new key
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % table_name
        conn.execute(ADD_ITEM, (encode(key), item))
        # delete record with old key
        DEL_ITEM = 'DELETE FROM %s WHERE key = ?' % table_name
        conn.execute(DEL_ITEM, (key,))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(module)s:%(lineno)d : %(funcName)s(%(threadName)s) : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    program = os.path.basename(sys.argv[0])

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    path = sys.argv[1]
    table_name = sys.argv[2]

    MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value BLOB)' % table_name
    conn = SqliteMultithread(path, autocommit=True, journal_mode="DELETE")
    conn.execute(MAKE_TABLE)
    conn.commit()

    migrate(path, table_name, conn)

    conn.close()

    logger.info("finished running %s", program)
