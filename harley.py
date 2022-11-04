#!/usr/bin/env python3

'''
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-04
'''

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


def get_webdriver():
	driver = webdriver.Firefox(service=Service(	# Init FF webdriver
		executable_path=GeckoDriverManager().install()))
	return driver

def process_cur_page(dealers):
	for dealer in dealers:
		dealer_name = dealer.find_element(By.CLASS_NAME, 'find__results__item__link').text
		dealer_address_and_phone = dealer.find_element(By.CLASS_NAME, 'b8').text.split('\n')
		dealer_address = dealer_address_and_phone[0]
		dealer_phone = dealer_address_and_phone[1]
		print('Name:\t	{}'.format(dealer_name))
		print('Address:\t{}'.format(dealer_address))
		print('Phone:\t	{}'.format(dealer_phone))
		print('---')

try:
	driver = get_webdriver()
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
	# Example num_results >> '50 dealers near Hudsonville, MI 49426, USA'
	num_dealers = int(num_results.text.split()[0])	# Get number of dealers from above string
	print('Number of dealers: {}'.format(num_dealers))

	# Wait for search results to load, TODO: if no results, exception is thrown
	WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
		(By.CLASS_NAME, 'find__results__list')))

	# Get number of search result pages
	results_pagination = int(driver.find_element(By.CLASS_NAME, 'find__results__pagination__page__total').text)
	print('Results pagination total: {}'.format(results_pagination))

	# For each search result page
	current_page = 1
	while (current_page <= results_pagination):
		print('Current Page: {}'.format(current_page))

		# Get list of dealers on current page
		dealers = driver.find_elements(By.CLASS_NAME, 'find__results__item')
		# Process dealers on current page
		process_cur_page(dealers)

		# Click on 'Next' page button, if enabled
		next_button = driver.find_element(By.CLASS_NAME, 'find__results__pagination__dir--next')
		if next_button.is_enabled():
			next_button.click()

		# End while loop
		current_page = current_page + 1

except Exception as err:
	print('Exception!')
	print(err)

finally:
	driver.quit()
	print('Done')
