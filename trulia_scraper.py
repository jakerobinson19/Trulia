import time
from selenium import webdriver

import trulia_functions as tl

if __name__=='__main__':

  zips = ['85017','85259','85281','85282','85033','85015','85258','85021','85020']
  full_data = []

  browser = webdriver.Chrome()

  tl.go_to_trulia(browser)

  pages = tl.get_number_of_pages(browser)
  print("{} pages".format(pages))
  loop = 1

  for zipcode in zips:
    output_data = []
    
    tl.check_for_captcha(browser)

    tl.go_to_trulia_url(browser,'rent',zipcode)

    tl.check_for_captcha(browser)

    pages = tl.get_number_of_pages(browser)
    print("{} pages".format(pages))

    for n in  range(pages):
      time.sleep(5)
      search_results = tl.get_listings(browser)

      print("{} Listings from this page".format(len(search_results)))

      for listing in search_results:
        try:
          listing = listing.text

          listing = listing.split('\n')
          
          listing.pop(-2)

          address = listing[-2]
          listing.pop(-2)

          abort = False

          for item in listing:
            if '$' in item:
              price = item.rstrip('/mo')
            
            elif 'bd' in item or 'Studio' in item:
              if '-' in item:
                abort = True
                break
              
              elif 'Studio' in item:
                bds = 0
              
              else:
                bds = item.rstrip('bd')
            
            elif 'ba' in item:
              bas = item.rstrip('ba')
           
            elif 'sqft' in item:
              sqft = item.rstrip(' sqft')
            
          if address == 0 or bds == 10 or bas == 0 or sqft == 0 or price == 0:
            abort = True

          if abort == True:
            continue
         
          else:
            price_per_sqft = tl.get_price_per_sqft(price,sqft)

            output_data.append([address,bds,bas,sqft,price,price_per_sqft])
            address = 0
            bds = 10
            bas = 0
            sqft = 0
            price = 0

        except Exception as e:
          print("Something went wrong: {}".format(e))
          continue

      tl.go_to_next_page(browser)

      tl.check_for_captcha(browser)
    #end of main function loop

    output_dataframe = tl.create_output_dataframe(output_data)

    sum_data = tl.get_summary_data(clean_data(output_dataframe))

    full_data.append([output_dataframe, sum_data])

    tl.write_data_to_file(full_data, zips)
