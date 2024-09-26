# Sp500 Stock income statement updater
 Made for fördjupad python programmerings course, kunskapskontroll 2

## purpose
- This project was made of the intention to keep track and download new quarterly income statements for the given companies.
- The chosen companies are included in the index sp500.
- The script tracks companies which have released new earnings and can then download and update the lastest quarterly income statement.
- An sql database is also created and exist in the git but the script to create a clean database are also included.

## Installation
The project also includes a virtual enviorment but if you wish to use your own enviorment then install the packages in the requirment.txt 

```bash
pip install -r requirements.txt
```

## Setup

There are 3 things to setup if you wish to setup everything yourself

- the list of companies in the index sp500
  This can be done using the sp500_list_getter module.
  #### sp500_list_getter module
  This module uses the request package to get the html data from our url.
  The given url: https://www.wikitable2json.com/api/List_of_S%26P_500_companies?table=0,
  is already in a readable json format which can be passed as a dataframe and give us the data we need
  The module also automaticly transforms the dataframe and can also add earnings dates to each of the given symbol in the index.

- Skippable step, saving to csv
  The create_sp500_list.py script uses the sp500_list_getter module to create and save the data as an .csv file
  This step may be skipped as the next step includes code to directly upload the data to the database
  #### NOTE
  keep in mind that making frequent request from sp500_list_getter module might overload the yfinance api and the webserver for the url

- Create database and include table with the sp500
  The setup_db.py script will create a database with the given name and at given path.
  It will also upload the dataframe to the database as a table.

## First run

if you are running the script for the first time you will need to create tables for each of the symbols and their income statement.
this is not included in the script but can easly be done using the 2 modules DBAccess and API

running the code below will download and create the list

```python
from access_db import DBAccess
from api import API
path = "" #your path
db = "Stock Database.db"
dbaccess = DBAccess(path,db)
api = API()
update_list = dbaccess.get_list_of_needed_updates()
#should give you the whole sp500 as none were last updated
api.add_list(update_list)
api.get_financials()
financials, failed_calls, time = api.get_all()
dbaccess.create_financial_table(financials)
dbaccess.update_last_update(time,update_list)
dbaccess.close_connection()
```
This code will download all the income statement for respektive symbol and creates a new table for them.
After this you may run the main.py as an updater
  
## Scheduler

The updater is run as main.py and it should also be setup as a schedule in task manager for continues running.
it can be run att any time daily,weekly or whenever but i strongly recommend to update everyday as there are often atleast 1 new report per day

#### main.py
the main is run whenever you would like to update the database.

keep in mind to change the varible path if needed if the location of the database is not within the working directory
```path
path = "" #edit if needed
```
the main.py will also log events in the Main_logfile.log
if something were to fail feel free to read the logs and act accordingly


#### DBAccess module
The DBAccess module is written to handle all changes read,writing and formatting for the database.
it is also used togheter with the API module to handle when or what to update.

#### API module
The API module is used mainly to download data using the yfinance api.
The yfinance api is a community written package made from yahoos api and used as a webscraper to gather financial information from yahoos own server.
The module also handles some formatting to fit into the database and the DBAccess module.


## tester.py

tester.py is a standard test using pytest to test both API and DBAccess modules.
there are currently 6 test, 4 DBAccess test and 2 API test.
Both are made to check if the classes handles exceptions, datatypes and attrributes correctly

## miscellaneous
- There are some other objects in this git, some are used as a working frame such as the database.png which was an early version of the database setup.
- there is also a bat filed used personally to set up the task scheduler, feel free to copy, change the respective directy. one to the pythin interpeter and the main.py file.
- There is also the pdf for the assignment and proof of task schedule setup.

# Thank you

i want to thank Linus Rundberg Streuli for being a great teacher and writing a great book with co writer Antonio Prgomet.
https://www.akademibokhandeln.se/bok/lar-dig-python-fran-grunden/9789181110500

# Author 
## Andreas Wendel
- https://www.linkedin.com/in/andreas-wendel-29081028b/




  
  
