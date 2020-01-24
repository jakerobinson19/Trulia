#!/usr/bin/env python
'''
WARNING: Use this code at your own risk, scraping is against Trulia's TOC.

Trulia home listings scraper, using Selenium.  The code takes as input search 
terms that would normally be entered on the Zillow home page.  It creates 5 
variables on each home listing from the data, saves them to a data frame, 
and then writes the df to a Excel file that gets saved to your working directory.

Software requirements/info:
- This code was written using Python 3.7.
- Scraping is done with Selenium v3.0.2, which can pip installed, or downloaded
  here: http://www.seleniumhq.org/download/
- The selenium package requires a webdriver program. This code was written 
  using Chromedriver v76, which can be downloaded here: 
  https://sites.google.com/a/chromium.org/chromedriver/downloads
  
'''

import time
import trulia_functions as tl

# Prior to run, update zips list to include the zipcodes you wish to scrape 
# Additionally, specify the listing_type you are interested (through the listing_type obj)
# Options are 'buy', 'rent', 'sold'

zips = ['85017','85259','85281','85282','85033','85015','85258','85021','85020']
  
city, state = 'Phoenix', 'AZ'

# Specify the listing type 
listing_type = 'buy'

# Initialize list obj that will house all scraped data
full_data = []

# Initialize the webdriver
browser = tl.init_driver('/usr/local/bin/chromedriver')

# Go to Trulia home page
tl.go_to_trulia(browser)

# start scraping
for zipcode in zips:
  # Initialize list obj that will hold the data for each zipcode
  output_data = []

  # Navigate to the url for the zipcode and listing type
  tl.go_to_trulia_url(browser,listing_type, zipcode, city, state)

  # Pull the number of pages of listing cards for the zipcode
  # If there are zero pages, it will move onto the next zipcode
  pages = tl.get_number_of_pages(browser)
  print("{} pages".format(pages))

  # For each page, pull the raw data from the listing cards
  for pg in range(pages):
    time.sleep(5)
    search_results = tl.get_listings(browser)

    print("{} Listings from this page".format(len(search_results)))

    # For each home listing, extract the 5 variables that will populate
    # the output dataframe (address, price, bds, bas, sqft)
    for listing in search_results:
      info = dict.fromkeys(["address","bds","bas","sqft","price"], None)
        
      try:
        listing = listing.text

        listing = listing.split('\n')
          
        if listing_type == 'rent':
          i = -2
        else:
          i = -1
        try:
          #remove the city, state, and address elements after assigning the address
          #elements are removed to avoid issues for later logic if they contain 'bd' or 'ba' 
          listing.pop(i)
          info['address'] = listing[i]
          listing.pop(i)

        except IndexError:
          continue

        abort = False

        # For each item in the list of listing details assign the values for 
        # price, bds, bas, and sqft based on observed string match
        for item in listing:
          # Price
          if '$' in item:
            info['price'] = item.rstrip('/mo')
            
          # Bedrooms
          elif 'bd' in item or 'Studio' in item:
            info['bds'] = item.rstrip('bd')
            
          # Bathrooms
          elif 'ba' in item:
              info['bas'] = item.rstrip('ba')
           
          # Square Footage
          elif 'sqft' in item:
            info['sqft'] = item.rstrip(' sqft')
        
        # Check if the data is reasonable. If it isn't, it will not be
        # added to the output data that is converted to the Excel file    
        if tl.validate_data(info.values()):
          continue
        # If data is valid, proceed to calculate price per square foot 
        else:
          info['price_per_sqft'] = tl.get_price_per_sqft(info['price'],info['sqft'])

          output_data.append(list(info.values()))
        #end loop assigning values for the listing

      except Exception as e:
        print("Something went wrong: {}".format(e))
        continue
      #end loop through page listings
      
    if pg == pages - 1:
      break
    else:
      tl.go_to_next_page(browser)
  #end loop through pages

  output_dataframe = tl.create_output_dataframe(output_data)

  sum_data = tl.get_summary_data(tl.clean_data(output_dataframe))

  full_data.append([output_dataframe, sum_data])

  tl.write_data_to_file(full_data, zips)
  #end loop through zipcodes
#end main
