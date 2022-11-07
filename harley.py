#!/usr/bin/env python3

'''
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-07
'''

import sqlite3
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


# ZIP_CODE = 49426    # Grand Rapids, MI
# ZIP_CODE = 99782    # Wainwright, AK - no results example
DATABASE_FILENAME = 'sql/harley.db'


def sanitize_phone(phone):
    for character in '()-+ ':
        phone = phone.replace(character, '')
    return phone

def sql_get_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILENAME)
    except Exception as e:
        print('Error connecting to {}: {}'.format(DATABASE_FILENAME, e))
    return conn

def sql_get_zip_codes(conn):
    cur = conn.cursor()
    cur.execute('SELECT zip_code FROM zip_codes WHERE search_completed=0;')
    rows = cur.fetchall()

    zip_codes = []
    for row in rows:
        zip_codes.append(row[0])

    return zip_codes

def sql_update_zip_code(conn, zip_code):
    cur = conn.cursor()
    cur.execute('UPDATE zip_codes SET search_completed=1, datetime_completed=datetime() WHERE zip_code=?;', (zip_code,))
    conn.commit()

def sql_add_dealer(conn, name, address, phone):
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO dealers (name, address, phone) VALUES (?, ?, ?);', (name, address, phone))
    conn.commit()


try:
    # Init DB
    conn = sql_get_connection()
    zip_codes = sql_get_zip_codes(conn)
    # Init Webdriver
    driver = webdriver.Firefox(service=Service(
        executable_path=GeckoDriverManager().install()))
    driver.get('https://www.harley-davidson.com/us/en/tools/find-a-dealer.html')
    enter_zip = driver.find_element('id', 'find-term')

    for zip_code in zip_codes:
        # Fill 'Enter ZIP, Address, or Dealer Name' field
        enter_zip.clear()
        enter_zip.send_keys(zip_code)

        # Wait for 'Search' button to load after zip code field is filled, click
        WebDriverWait(driver, 6).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'find__form__submit__button'))).click()

        # Get search results
        try:
            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CLASS_NAME, 'find__results__list')))
        except:
            # No search results
            sql_update_zip_code(conn, zip_code)
            continue

        # Get number of search result pages
        results_pagination = int(
            driver.find_element(
                By.CLASS_NAME,
                'find__results__pagination__page__total').text)

        # For each search result page
        current_page = 1
        while (current_page <= results_pagination):
            # Get list of dealers on current page
            dealers = driver.find_elements(By.CLASS_NAME, 'find__results__item')
            # Process dealers on current page
            for dealer in dealers:
                # Get name
                name = dealer.find_element(
                    By.CLASS_NAME, 'find__results__item__link').text

                # Get contact
                contact = dealer.find_element(
                    By.CLASS_NAME, 'b8').text.split('\n')

                # Get address from contact
                address = contact[0]

                # Get phone from contact, if exists
                if len(contact) > 1:
                    phone = sanitize_phone(contact[1])
                else:
                    phone = None

                # Add dealer to DB, duplicates ignored via query
                sql_add_dealer(conn, name, address, phone)

            # Click on 'Next' page button, if enabled
            next_button = driver.find_element(
                By.CLASS_NAME, 'find__results__pagination__dir--next')
            if next_button.is_enabled():
                next_button.click()

            # End current search page
            current_page = current_page + 1

        # End current zip code search
        sql_update_zip_code(conn, zip_code)
        print('Finished searching {}'.format(zip_code))

    # Done
    if driver: driver.quit()
    if conn: conn.close()
    print('Done')

except:
    # if driver: driver.quit()
    if conn: conn.close()
    traceback.print_exc()
