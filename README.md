# trulia_data_scraper
Scrape data from trulia.com using selenium and python

ATTENTION
---------
Trulia can detect the automated webdriver and will throw a captcha. However, the bot will pause anytime a captcha appears and wait for the user to solve the captcha to continue scraping data. Although not entirely automated because of this required interaction, the bot can still reasonably scrape listing data for several zipcodes in between interruption.


WARNING: Use this code at your own risk, scraping is against Trulia's TOC
-------------------------------------------------------------------------

Basic tool for scraping current home listings from Trulia, written in Python using Selenium. The code takes as input search terms that would normally be entered on the Trulia home page. It creates 5 variables on each home listing from the data, saves them to a dataframe, and then writes the df to a CSV file that gets saved to your working directory.

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
