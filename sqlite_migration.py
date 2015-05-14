#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code is distributed under the terms and conditions
# from the Apache License, Version 2.0
#
# http://opensource.org/licenses/apache2.0.php

"""
USAGE: %(program)s sqlitedict_old_path sqlitedict_new_path [tablename (optional)]

This is the compatibility script to migrate the sqlite DB from version that is compatible with sqlitedict 1.x
to the version compatible with sqlitedict 2.x
"""
import logging
import os
import sys

from sqlitedict import encode, SqliteMultithread

logger = logging.getLogger(__name__)


def migrate(table_name, conn_old, conn_new):
    # get all old keys
    GET_KEYS = 'SELECT key FROM %s ORDER BY rowid' % table_name
    old_keys = [key[0] for key in conn_old.select(GET_KEYS)]
    for pos, key in enumerate(old_keys):
        if pos % 100 == 0:
            logger.info("converted %ith element of the DB", pos)
        # get value for the given key
        GET_ITEM = 'SELECT value FROM %s WHERE key = ?' % table_name
        item = conn_old.select_one(GET_ITEM, (key,))
        # save record with new key to new sqlite DB
        ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % table_name
        conn_new.execute(ADD_ITEM, (encode(key), item[0]))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(module)s:%(lineno)d : %(funcName)s(%(threadName)s) : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    program = os.path.basename(sys.argv[0])

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    path_old = sys.argv[1]
    path_new = sys.argv[2]

    if len(sys.argv) == 4:
        table_name = sys.argv[3]
    else:
        table_name = 'unnamed'

    MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value BLOB)' % table_name
    conn_old = SqliteMultithread(path_old, autocommit=True, journal_mode="DELETE")
    conn_old.execute(MAKE_TABLE)
    conn_old.commit()

    conn_new = SqliteMultithread(path_new, autocommit=True, journal_mode="DELETE")
    conn_new.execute(MAKE_TABLE)
    conn_new.commit()

    migrate(table_name, conn_old, conn_new)

    conn_old.close()
    conn_new.close()

    logger.info("finished running %s", program)
