import sqlite3
import pandas as pd
import datetime as dt
import logging


logger = logging.getLogger()
    

class DBAccess():
    def __init__(self,path,db) -> None:
        """
        Initalising connection to database.

        Args:
            path (str): path to database from python
            db (str): name of database.db
        """
        
        mode = "?mode=rw" 
        #using mode and uri=true to raise error if database doesn't exist
        #rw = read & write
        #otherwise it will create a new database
        try:
            self.conn = sqlite3.connect("file:"+path+db+mode, uri=True)
        except sqlite3.Error as e:
            logger.exception(e)
            print(e)
            print("Database doesn't exist")
            logger.warning("give database doesn't exist, check path")
            raise
        
                
    def get_list_of_needed_updates(self):
        """
        Gets the sp500 dataframe from sql and calculates which symbols
        needs to be updated after earnings.
        Also updates the current values in table.
        
        Returns:
            list: list of symbols which needs to update, send to api
        """
        
        #defined by datetime, present is greater than past
        today = dt.datetime.today()
        df = pd.read_sql_query('SELECT * FROM SP500', self.conn)
        df = df[["Symbol","Earnings date","Last update"]]
        df["Earnings date"] = pd.to_datetime(df["Earnings date"], yearfirst=True)
        df["Last update"] = pd.to_datetime(df["Last update"], yearfirst=True)
        df["Need update"] = (
                            (((df["Earnings date"]+ dt.timedelta(days=1)) <= today) & 
                            (df["Last update"] <= (df["Earnings date"] + dt.timedelta(days=1)))) |
                            (df["Last update"] < (today - dt.timedelta(days=730))) 
                            )
        #Checking if its time to update
        #also check if last update is longer than 2 years
        
        update_list = []
        for i in range(len(df)):
            if df["Need update"][i] == True:
                update_list.append(df["Symbol"][i])
        #skapar lista som returneras
        
        sql = 'UPDATE SP500 SET "Need update" = ? WHERE Symbol = ?'
        for i in range(len(df["Symbol"])):
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql, (df["Need update"][i].item(),df["Symbol"][i]))
                #item() is used as sql can't handle np.true_/false_
                #item() returns the classic python True/False which sql can handle
                self.conn.commit()
            except sqlite3.Error as e:
                logger.exception(e)
                print(e)
        #update sql table
        if not update_list:
            logging.info("Nothing to update")
        
        return update_list      
    
    
    def check_earnings_last_update(self):
        """
        Checks the table sp500 if there are old earnings date.
        Some companies might not have given a new date therefor an old date is in the api.

        Returns:
            list: list of symbols which need their earnings date updated
        """
        df = pd.read_sql_query('SELECT * FROM SP500', self.conn)
        df = df[["Symbol","Earnings date","Last update"]]
        symbols = []
        for i in range(len(df)):
            if df["Earnings date"][i] < df["Last update"][i] == True:
                symbols.append(df["Symbol"][i])
                
        return symbols         
         
          
    def update_earnings_date(self,df):
        """
        Update earnings date column in sp500 table
        for given symbols.

        Args:
            df (pandas.DataFrame): dataframe with symbols and respective earnings date
        """
        
        sql = 'UPDATE SP500 SET "Earnings date" = ? WHERE Symbol = ?'
        for i in range(len(df["Symbol"])):
            time = df["Earnings date"][i].strftime("%Y-%m-%d %H:%M:%S")
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql, (time,df["Symbol"][i]))
                self.conn.commit()
            except sqlite3.Error as e:
                logger.exception(e)
                print(e)
 
 
    def update_last_update(self,time,financial_list):
        """
        update last update column in sp500 table.

        Args:
            time (str): timestamp of downloaded financials in str datatype
            financial_list (list): list of symbols which has been updated
        """
        
        sql = 'UPDATE SP500 SET "Last update" = ? WHERE Symbol = ?'
        symbol = financial_list
        for i in range(len(symbol)):
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql, (time,symbol[i]))
                self.conn.commit()
            except sqlite3.Error as e:
                logger.exception(e)
                print(e)
                
                
    def create_financial_table(self,list):
        """
        Create new table for financial information.
        Ex new symbol added for sp500 or create balance sheet, cashflow statements.

        Args:
            list (list): list which contrains dataframes in each element
        """
        
        for i in range(len(list)):
            df = list[i]
            df.to_sql(df["Symbol"].iloc[0], self.conn, if_exists="replace")
          
            
    def insert_financial_data(self,list_of_df):
        """
        Insert new data in income statement table for given symbol.
        Also checks new data has been update since the last if not,
        returns a list for the symbol with old data.
        Cause is probably that the api has not updated that data even though the earnings is released.

        Args:
            list_of_df (list): list of dataframes with income statements

        Returns:
            list: list of symbols which did not include new data
        """
        
        failed_update = []
        for i in range(len(list_of_df)):
            symbol = list_of_df[i]["Symbol"].iloc[0]
            query = (f'SELECT * FROM {symbol}')
            df = pd.read_sql_query(query, self.conn)
            list_time = list_of_df[i].index[-1]
            df_time = dt.datetime.strptime(df["index"].iloc[-1], '%Y-%m-%d %H:%M:%S')
            if list_time == df_time:
                print(symbol +" Already up to date")
                logging.warning(symbol+" Table already up to date, should not happen check api or yahoo finance")
                failed_update.append(symbol)
            else:
                try:
                    df_insert = list_of_df[i].tail(1)
                    df_insert.to_sql(symbol, self.conn, if_exists="append")
                    #if_exists="append" insert the dataframe into an existing table instead of creating/replacing
                    logging.info(symbol + " has been updated")
                except sqlite3.Error as e:
                    logger.exception(e)
                    print(e)
                    
        return failed_update    
    
    
    def close_connection (self):
        """
        Closes connection.
        Always close connection.
        """
        self.conn.close()
