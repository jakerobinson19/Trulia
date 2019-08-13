from trulia_functions import get_listings
from trulia_functions import go_to_next_page
from trulia_functions import write_data_to_file

import time

if __name__=='__main__':
  output_data = []

  browser = webdriver.Chrome()

  go_to_trulia(browser)
  
  zipcode = input("What zipcode would you like to get rent data for? ")
  
  browser.get('https://www.trulia.com/for_rent/{}_zip/'.format(zipcode))

  inp = input("---------------\nDo you wish to continue with scraping? ")


  #get number of pages of rentals for the zipcode
  pages = get_number_of_pages(browser)

  if inp == 'y':

    while loop < pages:
      time.sleep(5)
      listings = get_listings(browser)

      '''Trulia listings cards return text in two possible formats:
            'PET FRIENDLY
             $1,281 – $1,830
             1 – 3bd
             1 – 2ba
             867 – 1,608 sqft
             La Privada at Scottsdale Ranch apartments
             Contact Property'
          
             or 
                
            '$2,200
             3bd
             2ba
             2,195 sqft
             8006 N Via Verde
             Contact Property'
                
           Spliting on the newlines will create a list of text. Based on the
           formatting above, the list will map onto the structure of 
           [..., (price), (bd,ba,sqft), (address), 'Contact Property'] 
              
           This means address will alway be second to last, rooms and sq footage 
           are third to last, and price comes just before that. In other words, 
           address = list[-2], rooms = list[-3], and price = list[-4]'''
              
      for l in listings:
        try:     
          #pull text from the listing and split on the newlines
          l = l.text
          l = l.split('\n')
          
          address = l[-3]

          for item in l:
            if '$' in item:
              price = item.rstrip('/mo')
            elif 'bd' in item:
              bds = item.rstrip('bd')
            elif 'ba' in item:
              bas = item.rstrip('ba')
            elif 'sqft' in item:
              sqft = item.rstrip(' sqft')
           '''
          address = l[-2]
          
          price = l[-4]
          
          details = l[-3]
          
          detailss = details.split('bd')
          bds = details.pop(0)
          
          details = details[0].split('ba')
          bas = details.pop(0)
          
          details = details[0].split(' ')
          sqft = details.pop(0)
          '''
          output_data.append([address,bds,bas,sqft,price])
        
        except Exception as e:
          print("something went wrong: {}".format(e))
          continue

      loop += 1
      go_to_next_page(browser)

    write_data_to_file(output_data, '85258')
