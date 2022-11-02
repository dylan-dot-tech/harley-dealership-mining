#!/usr/bin/env python3

"""
@author: dylan.tech
@contact: hi@dylan.tech
@copyright: https://dylan.tech
@version: 2022-11-02
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


BASE_URL = 'https://www.harley-davidson.com/us/en/tools/find-a-dealer.html'
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
driver.get(BASE_URL)

zip_code = 49417

enter_address = driver.find_element('id', 'find-term')
enter_address.clear()
enter_address.send_keys(zip_code)

# Click 'Find' button, doesn't appear until after the zip_code was entered
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'find__form__submit__button'))).click()

# Get number of dealers near zip_code (caps at 50)
num_results = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'find__results__head__count'))).text
print(num_results)
# Get number of search result pages
results_pagination = driver.find_element(By.CLASS_NAME, 'find__results__pagination__page__total').text

# Done
driver.close()
print('Done')
