import trulia_functions as tl
from trulia_functions import go_to_next_page
from trulia_functions import write_data_to_file

import time

if __name__=='__main__':

  zips = ['28215','28227','28213','28212','28210','28208','28205','28105','28269']
  full_data = []
  
  browser = webdriver.Chrome()

  tl.go_to_trulia(browser)

  zipcode = input("Enter the zipcode you would like to scrape data for: ")

  #inp = input("Do you wish to continue with scraping? ")

  pages = tl.get_number_of_pages(browser)
  print("{} pages".format(pages))
  loop = 1

  for zipcode in zips:
    output_data = []
    captcha = tl.check_for_captcha(browser)

    if captcha:
      while True:
        resume = input("Enter 'y' once you have completed the captcha: ")
        if resume == 'y':
          #captcha = check_for_captcha(browser)
          #if captcha:
          break

    browser.get('https://www.trulia.com/for_rent/'+ zipcode +'_zip/')

    captcha = tl.check_for_captcha(browser)

    if captcha:
      while True:
        resume = input("Enter 'y' once you have completed the captcha: ")
        if resume == 'y':
          #captcha = check_for_captcha(browser)
          #if captcha:
          break

    pages = tl.get_number_of_pages(browser)
    print("{} pages".format(pages))
    loop = 1

    while loop <= pages:
      time.sleep(5)
      listings = tl.get_listings(browser)

      print("{} Listings from this page".format(len(listings)))

      for l in listings:
        try:
          l = l.text

          l = l.split('\n')
          
          address = l[-3]
          l.pop(-3)

          abort = False

          for item in l:
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
            output_data.append([address,bds,bas,sqft,price])
            address = 0
            bds = 10
            bas = 0
            sqft = 0
            price = 0

        except Exception as e:
          print("Something went wrong: {}".format(e))
          continue

      loop += 1
      tl.go_to_next_page(browser)

      captcha = tl.check_for_captcha(browser)

      if captcha:
        while True:
          resume = input("Enter 'y' once you have completed the captcha: ")
          if resume == 'y':
            #captcha = check_for_captcha(browser)
            #if captcha:
            break


    #print(output_data)

    output_dataframe = tl.create_output_dataframe(output_data)

    sum_data = tl.get_summary_data(output_dataframe)

    full_data.append([output_dataframe, sum_data])
    tl.write_data_to_file(full_data, zips)
