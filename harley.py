#!/usr/bin/env python3

"""
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-03
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


BASE_URL = 'https://www.harley-davidson.com/us/en/tools/find-a-dealer.html'
zip_code = 49426    # Grand Rapids, MI
# zip_code = 99782    # Wainwright, AK - no results example

try:
	# Init webdriver
	driver = webdriver.Firefox(service=Service(
		executable_path=GeckoDriverManager().install()))
	driver.get(BASE_URL)

	# Select 'Enter Zip, Address, or Dealer Name' field
	enter_zip = driver.find_element('id', 'find-term')
	# Fill zip code field
	enter_zip.clear()
	enter_zip.send_keys(zip_code)

	# Wait for 'Search' button to load after zip code field is filled, click
	# when available
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
		(By.CLASS_NAME, 'find__form__submit__button'))).click()

	# Get number of dealers near zip code, caps at 50
	num_results = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'find__results__head__count')))
	# Example num_results >> "50 dealers near Hudsonville, MI 49426, USA"
	num_dealers = int(num_results.text.split()[0])	# Get number of dealers from above string
	print("Number of dealers: {}".format(num_dealers))

	# Wait for search results to load, TODO: if no results, exception is thrown
	WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
		(By.CLASS_NAME, 'find__results__list')))

	# Get number of search result pages
	results_pagination = driver.find_element(By.CLASS_NAME, 'find__results__pagination__page__total').text
	print('Results pagination total: {}'.format(results_pagination))

	# Get list of dealers from current page
	dealer_list = driver.find_element(By.CLASS_NAME, 'find__results__list')
	dealers = dealer_list.find_elements(By.TAG_NAME, 'li')

	# For each dealer listed on current page
	for dealer in dealers:
		text = dealer.text
		print(text)
		print('---')

except Exception as err:
	print("Exception!")
	print(err)

finally:
	driver.close()
	print('Done')
