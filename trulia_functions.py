#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import pandas as pd
from pandas import ExcelWriter
import numpy as np

xpath {
  'listing_cards':'//*[@class="xsCol12Landscape smlCol12 lrgCol8"]',
  'address':'tyuio',
  'price':'ghjkl',
  'bdr':'asf',
  'ba':'asf',
  'sqft':'asfd'
}


def go_to_trulia(browser):
  browser.get('https://www.trulia.com/')
  
def get_listings(browser):
  try:
    listing_cards = WebDriverWait(browser, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, xpath['listing_cards']))
    )
  except (NoSuchElementException, TimeoutException):
    try:
      listing_cards = WebDriverWait(browser, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-183kqex-3 hxSIvC"]'))
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

'''Find the number of the last page of listing results to inform how many pages to loop through'''
def get_number_of_pages(browser):
  try:
    pages = browser.find_elements_by_xpath('//li[@data-testid="pagination-page-link"]')
    pages_num = int(pages[-1].text)

  except:
    try:
      pages = browser.find_elements_by_xpath('//a[@class="pvl phm"]')
      pages_num = int(pages[-1].text)

    except Exception as e:
      print("Unable to get number of pages - {}".format(e))
      pages_num = 1

  return(pages_num)

'''Find the next page arrow for listing results and click it'''
def go_to_next_page(browser):
  try:
    nextp = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//i[@class="iconRightOpen"]')))
    nextp.click()
  
  except (NoSuchElementException, TimeoutException):
    try:
      nextp = WebDriverWait(browser, 10).until(
              EC.visibility_of_element_located((By.XPATH, '//li[@data-testid="pagination-next-page"]')))
      nextp.click()
    except:
      print("Unable to get next page - abort")

def get_summary_data(data):
  #set studios to bedrooms = 0
  data.loc[data['Bedrooms'] == 'Studio', 'Bedrooms'] = 0
  
  #formatting data to allow aggregation
  data['Bedrooms'] = data.Bedrooms.astype(int)
  data['Bathrooms'] = data.Bathrooms.astype(float)
  data['Sqft'] = data.Sqft.str.replace(',','').astype(int)
  data['Price'] = data.Price.str.replace('$','')
  data['Price'] = data.Price.str.replace(',','').astype(int)
  

  sum_data = data.groupby(['Bedrooms','Bathrooms']).agg({'Sqft':['min','max'], 'Price':['min','max','mean']})

  return(sum_data)      
      
def create_output_dataframe(output_data):
  columns = ["Address", "Bedrooms", "Bathrooms", "Sqft", "Price"]
  output_dataframe = pd.DataFrame(output_data, columns = columns).drop_duplicates()

  return(output_dataframe)

def write_data_to_file(list_dfs, zipcode):
    file_name = 'Rents_'+ zipcode + '.xlsx'
    xls_path = '/Users/admin/Desktop/trulia_scraper/' + file_name

    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            if n == 0:
              df.to_excel(writer, 'Rents - ' + zipcode)
            if n == 1:
              df.to_excel(writer, 'Summary - ' + zipcode)
        writer.save()
