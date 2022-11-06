#!/usr/bin/env python3

'''
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-06
'''

import sqlite3


DATABASE_NAME = 'harley.db'
QUERY_CREATE_TABLE = '''CREATE TABLE "dealers" (
    "name"	TEXT NOT NULL,
    "address"	TEXT NOT NULL UNIQUE,
    "phone"	TEXT,
    "added"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("address")
);'''


try:
    # Connect to DB
    conn = sqlite3.connect(DATABASE_NAME)
    curs = conn.cursor()

    # Create table
    curs.execute(QUERY_CREATE_TABLE)

    # Write changes to DB
    conn.commit()
    print('Done')

except Exception as e:
    print('ERROR: {}'.format(e))
