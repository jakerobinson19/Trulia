# Trulia Data Scraper
Scrape data from trulia.com using selenium and python

WARNING: Use this code at your own risk, scraping is against Trulia's TOC
-------------------------------------------------------------------------

Basic tool for scraping current home listings from Trulia, written in Python using Selenium. The code takes as input a list of zipcodes and whether to browse listing to buy, rent, or those that have been recently sold on Trulia. It creates 5 variables on each home listing, saves them to a dataframe, and then writes the df to a excel file, with a separate sheet for each zipcode, that gets saved to your working directory. The program also generates summary data which can be configured to show averages or min/max, its defaulted to show the min/max and mean of sqft and price grouped by the bedrooms and bathrooms (as shown below).

There are two files, trulia_scraper.py and trulia_functions.py. Clone this repo to your working directory, open the scraper file and step through the code line-by-line. The trulia functions are sourced at the top of the runfile.

Some things to keep in mind:
----------------------------
* You will need to edit the input parameter of function init_driver within zillow_runfile.py to point to the local path of your web driver program (required by Selenium).
* Zillow will periodically throw up a CAPTCHA page. The script is designed to pause scraping indefinitely until the user has manually completed the CAPTCHA requirements (at which point it should resume scraping).

Software Requirements/Info
--------------------------
- This code was written using [Python 3.7](https://www.python.org/downloads/).
- [Selenium](http://www.seleniumhq.org/download/) (this can be PIP installed, written using v3.0.2).
- The Selenium package requires a webdriver program. This code was written 
using [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) v2.25.

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
		                   Sqft		        Price		
		                min	max	   min	 max	mean
Bedrooms	Bathrooms					
2	          1.5	        930	930	  1079	1079	1079
            	    2	       1357	1706	  1250	2000	1633.3
	          2.5	        930	1582	  1095	2000	1331.4
	            3	       1085	1085	  1150	1150	1150
3	            1	       1320	1320	  1350	1350	1350
	            2	       1024	3105	  1000	2700	1582.5
	          2.5	       1344	2632	  1245	1950	1527.9                  
                                   
```
