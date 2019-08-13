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
              
           Then looping through the listings text, checking if it contains
           basic keywords and then append the desired info in a list which is
           then converted into a dataframe and written to a csv file'''
              
      for card in listings:
        try:     
          #pull text from the listing and split on the newlines
          card = card.text
          card = card.split('\n')
          
          address = card[-3]
          card.pop(-3)

          for item in card:
            if '$' in item:
              price = item.rstrip('/mo')
            elif 'bd' in item:
              bds = item.rstrip('bd')
            elif 'ba' in item:
              bas = item.rstrip('ba')
            elif 'sqft' in item:
              sqft = item.rstrip(' sqft')
       
          output_data.append([address,bds,bas,sqft,price])
        
        except Exception as e:
          print("something went wrong: {}".format(e))
          continue

      loop += 1
      go_to_next_page(browser)

    write_data_to_file(output_data, '85258')
