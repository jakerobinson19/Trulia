# Trulia Data Scraper
Scrape data from trulia.com using selenium and python

WARNING: Use this code at your own risk, scraping is against Trulia's TOC
-------------------------------------------------------------------------

Basic tool for scraping current home listings from Trulia, written in Python using Selenium. The code takes as input a list of zipcodes and whether to browse listing to buy, rent, or those that have been recently sold on Trulia. It creates 5 variables on each home listing, saves them to a dataframe, and then writes the df to a excel file, with a separate sheet for each zipcode, that gets saved to your working directory. The program also generates summary data which can be configured to show averages or min/max, its defaulted to show the min/max and mean of sqft and price grouped by the bedrooms and bathrooms (as shown below).

There are two files, trulia_scraper.py and trulia_functions.py. Clone this repo to your working directory, open the scraper file and step through the code line-by-line. The trulia functions are sourced at the top of the runfile.

Some things to keep in mind:
----------------------------
* You will need to edit the input parameter of function init_driver within trulia_scraper.py to point to the local path of your web driver program (required by Selenium).
* Trulia will periodically throw up a CAPTCHA page. The script is designed to pause scraping indefinitely until the user has manually completed the CAPTCHA requirements (at which point it should resume scraping).

Software Requirements/Info
--------------------------
- This code was written using [Python 3.7](https://www.python.org/downloads/).
- [Selenium](http://www.seleniumhq.org/download/) (this can be PIP installed, written using v3.0.2).
- The Selenium package requires a webdriver program. This code was written 
using [Chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/) v76.0.3809.

Usage
----------------------------
In trulia_scraper.py configure the zipcodes and types of properties you wish to scrap for ('buy' or 'rent') and save it.
```sh
zips = ['85017','85259','85281','85282','85033','85015','85258','85021','85020']

# Specify the listing type 
listing_type = 'buy'
```
Run the program from the command line:
```sh
python3 trulia_scraper.py
```
* Note: This will bring up a browser where selenium with scrape from trulia.com. You will have to solve captchas and tell the program to resume each time a captcha interrupts the process (which is hopefully not too often)

Example of the output dataframe
-------------------------------

```py
df.head(n = 5)
```

```
                 address     bedrooms  bathrooms    sqft    rent 
0      3011 Bissonnet St          1         1       991   $1795    
1          4229 Drake St          3         2     1,980   $2200     
2        2237 Wroxton Rd          2         2     1,500   $2500    
3      4318 Childress St          3         2     1,964   $2500     
4       2708 Werlein Ave          3         2     1,496   $1995 
```

Example of Summary Data
-----------------------

```
		                   Sqft		        Price		 $/sq
		             min    max   mean	   min	 max	mean     mean
Bedrooms	Bathrooms					
2	          1.5	     930    930	   930    1079	1079   1079	 1.16
            	    2	    1357   1706	  1531    1250	2000   1633.3	 1.07
	          2.5	     930   1582	  1340    1095	2000   1331.4    1.02
	            3	    1085   1085	  1085    1150	1150   1150	 1.06
3	            1	    1320   1320	  1320    1350	1350   1350	 1.02
	            2	    1020   3105	  2323    1000	2700   1582.5    0.68
	          2.5	    1344   2632	  1945    1245	1950   1527.9    0.78              
                                   
```
