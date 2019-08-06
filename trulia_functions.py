#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import time
import pandas as pd
import numpy as np

xpath {
  'address':'tyuio',
  'price':'ghjkl',
  'bdr':'asf',
  'ba':'asf',
  'sqft':'asfd'
}


def go_to_trulia(browser):
  browser.get('https://www.trulia.com/')
  
def get_listings(browser):
  listing_cards = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, xpath['listing_cards']))
  )   
    return(listing_cards)

def get_listing_info(browser, info_type):
  try:
    attr = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath[info_type]))).text
  
  except (NoSuchElementException, TimeoutException):
    attr = np.nan
    
  return(attr)

def write_data_to_file(output_data, zipcode):
    file_name = 'Rents_'+ zipcode + '.csv'
    columns = ["Address", "Bedrooms", "Bathrooms", "Sqft", "Price"]
    pd.DataFrame(output_data, columns = columns).drop_duplicates().to_csv(
    file_name, index = False, encoding = "UTF-8")
