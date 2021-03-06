#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import time
from datetime import date
import pandas as pd
from pandas import ExcelWriter
import numpy as np

# old xpaths
# listing_cards2':'//div[@class="Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-183kqex-3 hxSIvC"] [Dead Dec 2019]

xpath = {
  'listing_cards':'//*[@class="xsCol12Landscape smlCol12 lrgCol8"]',
  'listing_cards2':'//div[@class="Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-183kqex-3 hxSIvC"]',
  'pages':'//li[@data-testid="pagination-page-link"]',
  'pages2':'//a[@class="pvl phm"]',
  'next_page':'//i[@class="iconRightOpen"]',
  'next_page2':'//li[@data-testid="pagination-next-page"]',
  'captcha':'/html/body/section/div[2]/div/h1'
}


def init_driver(file_path):
  # Start browser in incognito mode to prevent cookies and disabled infobars
  options = webdriver.ChromeOptions()
  options.add_argument("incognito")
  options.add_argument("disable-infobars")
  driver = webdriver.Chrome(executable_path=file_path, 
                              chrome_options=options)
  driver.wait = WebDriverWait(driver, 10)
  return(driver)

def go_to_trulia(browser):
  browser.get('https://www.trulia.com/')

  check_for_captcha(browser)

def go_to_trulia_url(browser, type, zipcode, city = None, state = None):
  if type == 'buy':
    if city and state:
      browser.get('https://www.trulia.com/{}/{}/{}/'.format(state,city,zipcode))

    else:
      city = input("What city is {} in? ".format(zipcode))
      state = input("What state is {} in? ".format(zipcode))
      browser.get('https://www.trulia.com/{}/{}/{}/'.format(state,city,zipcode))

  elif type == 'rent':
    browser.get('https://www.trulia.com/for_rent/'+ zipcode +'_zip/')

  elif type == 'sold':
    browser.get('https://www.trulia.com/sold/'+zipcode+'_zip/')

  check_for_captcha(browser)

def go_to_next_page(browser):
  try:
    nextp = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath['next_page'])))
    nextp.click()
  
  except (NoSuchElementException, TimeoutException):
    try:
      nextp = WebDriverWait(browser, 10).until(
              EC.visibility_of_element_located((By.XPATH, xpath['next_page2'])))
      nextp.click()
    except:
      print("Unable to get next page - abort")

  check_for_captcha(browser)

def get_current_url(browser):
    """ Get URL of the loaded webpage """
    try:
        current_url = browser.execute_script("return window.location.href")

    except WebDriverException:
        try:
            current_url = browser.current_url

        except WebDriverException:
            current_url = None

    return current_url
  
def get_listings(browser):
  try:
    listing_cards = WebDriverWait(browser, 6).until(
      EC.presence_of_all_elements_located((By.XPATH, xpath['listing_cards']))
    )
  except (NoSuchElementException, TimeoutException):
    try:
      listing_cards = WebDriverWait(browser, 6).until(
      EC.presence_of_all_elements_located((By.XPATH, xpath['listing_cards2']))
      )
    except:   
      print("Unable to get listing cards - abort")
      listing_cards = np.nan

  return(listing_cards)

def get_listing_info(browser, info_type):
  try:
    attr = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath[info_type]))).text
  
  except (NoSuchElementException, TimeoutException):
    attr = np.nan
    
  return(attr)

def get_number_of_pages(browser):
  try:
    pages = browser.find_elements_by_xpath(xpath['pages'])
    pages_num = int(pages[-1].text)

  except:
    try:
      pages = browser.find_elements_by_xpath(xpath['pages2'])
      pages_num = int(pages[-1].text)

    except Exception as e:
      print("Unable to get number of pages - {}".format(e))
      pages_num = 1

  return(pages_num)

def clean_data(data):
  data.loc[data['Bedrooms'] == 'Studio', 'Bedrooms'] = 0
  data['Bedrooms'] = data.Bedrooms.astype(int)
  data['Bathrooms'] = data.Bathrooms.astype(float)
  data['Sqft'] = data.Sqft.str.replace(',','').astype(int)
  data['Price'] = data.Price.str.replace('$','')
  data['Price'] = data.Price.str.replace(',','').astype(int)

  return(data)

def validate_data(data):
  # Ignore data with invalid data and ranges (most likely apt complexes)
  for item in data:
    if item == 0 or item is None or '-' in item:
      return(True)

  return(False)

def get_price_per_sqft(price, sqft):
  p = price.replace('$','')
  p = int(p.replace(',',''))

  ppersq = round(p/(int(sqft.replace(',',''))),2)

  return(ppersq)

def get_summary_data(data):

  sum_data = data.groupby(['Bedrooms','Bathrooms']).agg({'Sqft':['min','max','mean'], 'Price':['min','max','mean'], '$/sq':'mean'})
  
  return(sum_data)

def create_output_dataframe(output_data):
  columns = ["Address", "Bedrooms", "Bathrooms", "Sqft", "Price", "$/sq"]
  output_dataframe = pd.DataFrame(output_data, columns = columns).drop_duplicates()

  return(output_dataframe)

def get_captcha(browser):
  try:
    h1 = browser.find_element_by_xpath(xpath['captcha']).text
    if 'verify' in h1:
      print("A wild Captcha has appeared!! Please solve it for me so I can continue :)")
      return(True)

    else:
      return(False)

  except:
      try:
        url = get_current_url(browser)
        if 'captcha' in url:
          print("A wild Captcha has appeared!! Please solve it for me so I can continue :)")
          return(True)

        else:
          return(False)

      except:
        return(False)

def check_for_captcha(browser):

  captcha = get_captcha(browser)

  if captcha:
    while captcha:
      
      resume = input("Enter 'y' once you have completed the captcha: ")
      
      if resume == 'y':
        captcha = get_captcha(browser)
        continue

def write_data_to_file(list_dfs, zipcodes):
    file_name = 'Listings_'+ str(date.today()) + '.xlsx'
    xls_path = '/Users/jakerobinson/Desktop/trulia_scraper/' + file_name

    with ExcelWriter(xls_path) as writer:
        for m, data in enumerate(list_dfs):
            for n, df in enumerate(data):
              if n == 0:
                df.to_excel(writer, 'Listings - ' + zipcodes[m])
              if n == 1:
                df.to_excel(writer, 'Summary - ' + zipcodes[m])
        writer.save()
