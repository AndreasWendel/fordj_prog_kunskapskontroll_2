import yfinance as yf
import datetime as dt
import pandas as pd
from time import sleep
import logging

logger = logging.getLogger()
"""
Notering. Yahoo har en limit request på x antal per min och y antal per timme
den kan bugga ur ibland.
yahoo räknar request per ip och att starta om datorn verkar funka.
möjligt att du har tur och får en ny dynamisk ip vilket kan göra att limiten resetar
i vilket fall så bör inte detta va ett problem i en schemalagd typ av updater.
"""
#^ändra till engelska

class API:
    def __init__(self) -> None:
        """
        Initializer
        """
        self.list = []
        self.list_of_error = []
        self.time = dt.datetime
        
    def add_list(self,list):
        """
        Add and/or resets the attribute List_of_companies
        aswell as resets the List attributes.
        used as a method to reset attribute without creating new instance

        Args:
            list (list): List of companies we want data for
        """
        
        self.list_of_companies = list
        self.list = []
        #clear list if run again
    
    def get_financials(self):
        """
        Downloads the financials statements from the given companies in quarterly format.
        The downloaded dataframe is also reformatted to match an sql table.
        The attribute time is also defined as a timestamp when the data was downloaded.
        
        """
        
        if not self.list_of_companies:
            logging.info("self.list_of_companies is empty")
            print("list is empty, provide list with .add_list()")
        else:
            for i in range(len(self.list_of_companies)):
                data = yf.Ticker(self.list_of_companies[i])
                income_stmt = data.quarterly_income_stmt
                
                if income_stmt.empty == True:
                    logging.WARNING(self.list_of_companies[i]+" Quarterly income DF is empty")
                    self.list_of_error.append(self.list_of_companies[i])
                else:
                    #formatting
                    income_stmt = income_stmt.T.iloc[::-1] 
                    income_stmt["Symbol"] = self.list_of_companies[i]
                    self.list.append(income_stmt)
                sleep(.1)
            self.time = dt.datetime.now()
            self.time = self.time.strftime("%Y-%m-%d %H:%M:%S")
        
            
    def get_earnings_date(self): 
        """
        download the earnings date for the given companies in list_of_companies.

        Returns:
            pandas.DataFrame: Dataframe of symbols and their respective upcoming earnings date
        """
        df = pd.DataFrame(self.list_of_companies, columns=["Symbol"])
        for i in range(len(self.list_of_companies)):
            try:
                ticker = yf.Ticker(self.list_of_companies[i])
                if len(ticker.calendar["Earnings Date"]) >= 1:
                    earning_date = ticker.calendar["Earnings Date"][0]
                else:
                    earning_date = None 
                    logger.warning("No earnings date was found for "+ self.list_of_companies[i]+ ", Date is set as None")
            except Exception as e:
                print(e)
                logging.warning(e)
                logging.warning("at "+ i)    
            df.at[i, "Earnings date"] = earning_date
        return df
            
    def get_list_of_df(self):
        """
        returns the list dataframes which include data of the respective company.

        Returns:
            list: list with dataframes
        """
        return self.list
    
    def get_list_of_failed_calls(self):
        """
        Gets list of companies which failed to download data.

        Returns:
            list: list with symbols which failed to download data
        """
        return self.list_of_error
        
    def get_timestamp_of_calls(self):
        """
        Gets timestamp of when data were downloaded.
        
        Returns:
            timestamp: timestamp
        """
        return self.time
    
    def get_all(self):
        """
        gets all relevant attributes.

        Returns:
            list,list,timestamp: returns list of df, list of failed calls and timestamp
        """
        return self.list, self.list_of_error, self.time
        