import time
from selenium import webdriver

import trulia_functions as tl

if __name__=='__main__':
  zips = ['85017','85259','85281','85282','85033','85015','85258','85021','85020']
  city, state = 'Phoenix', 'AZ'
  #listing_type: options are 'rent' 'buy' or 'sold'
  listing_type = 'buy'
  
  full_data = []

  browser = webdriver.Chrome()

  tl.go_to_trulia(browser)

  for zipcode in zips:
    output_data = []
    
    tl.check_for_captcha(browser)

    tl.go_to_trulia_url(browser,'rent',zipcode)

    tl.check_for_captcha(browser)

    pages = tl.get_number_of_pages(browser)
    print("{} pages".format(pages))

    for pg in range(pages):
      time.sleep(5)
      search_results = tl.get_listings(browser)

      print("{} Listings from this page".format(len(search_results)))

      for listing in search_results:
        info = dict.fromkeys(["price","bds","bas","sqft"], None)
        
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
            address = l[i]
            listing.pop(i)

          except IndexError:
            continue

          abort = False

          #loop through listing details and assign values for price, bds, bas, and sqft
          for item in listing:
            #price
            if '$' in item:
              info['price'] = item.rstrip('/mo')
            
            #bedrooms
            elif 'bd' in item or 'Studio' in item:
              #ignore listings with ranges (most likely apt complexes)
              if '-' in item:
                abort = True
                break
              
              elif 'Studio' in item:
                info['bds'] = 0
              
              else:
                info['bds'] = item.rstrip('bd')
            
            #bathrooms
            elif 'ba' in item:
              info['bas'] = item.rstrip('ba')
           
            #square footage
            elif 'sqft' in item:
              info['sqft'] = item.rstrip(' sqft')
            
          abort = tl.validate_data(info.values())

          if abort:
            continue
         
          else:
            price_per_sqft = tl.get_price_per_sqft(info['price'],info['sqft'])

            output_data.append([info.values(), price_per_sqft])
          #end loop assigning values for the listing

        except Exception as e:
          print("Something went wrong: {}".format(e))
          continue
        #end loop through page listings

      tl.go_to_next_page(browser)

      tl.check_for_captcha(browser)
    #end loop through pages

    output_dataframe = tl.create_output_dataframe(output_data)

    sum_data = tl.get_summary_data(clean_data(output_dataframe))

    full_data.append([output_dataframe, sum_data])

    tl.write_data_to_file(full_data, zips)
  #end loop through zipcodes
#end main
