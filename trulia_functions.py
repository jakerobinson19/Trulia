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

def go_to_trulia(browser):
  browser.get('https://www.trulia.com/')
  
get_listings(browser):
  listing_cards = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, xpath['listing_cards']))
  )   
    return(listing_cards)

get_listing_info
