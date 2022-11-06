#!/usr/bin/env python3

'''
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-06
'''

import csv
import sqlite3


DATABASE_NAME = 'harley.db'
ZIP_CODE_NAME = 'ZIP_Locale_Detail.csv'	# Source: https://postalpro.usps.com/ZIP_Locale_Detail

QUERY_CREATE_TABLE = '''CREATE TABLE zip_codes (
	"zip_code"	TEXT NOT NULL UNIQUE,
	"city"	TEXT NOT NULL,
	"state"	TEXT NOT NULL,
	"search_complete"	INTEGER NOT NULL DEFAULT 0,
	"last_updated"	TEXT,
	PRIMARY KEY("zip_code"));'''

QUERY_ADD_ZIP_CODE = 'INSERT OR IGNORE INTO zip_codes (zip_code, city, state) VALUES (?, ?, ?);'


try:
    # Connect to DB
    conn = sqlite3.connect(DATABASE_NAME)
    curs = conn.cursor()

    # Create table
    curs.execute(QUERY_CREATE_TABLE)

    # Seed .csv into DB
    reader = csv.reader(open(ZIP_CODE_NAME, 'r'))
    next(reader, None)  	# skip the headers
    for row in reader:
        city = row[7]		# Column labled 'Physical City'
        state = row[8]		# Column labled 'Physical State'
        zip_code = row[9]  	# Column labled 'Physical Zip'
        payload = [zip_code, city, state]
        curs.execute(QUERY_ADD_ZIP_CODE, payload)

    # Write changes to DB
    conn.commit()
    print('Done')

except Exception as e:
    print('ERROR: {}'.format(e))
