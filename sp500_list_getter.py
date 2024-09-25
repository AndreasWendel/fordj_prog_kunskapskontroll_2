import yfinance as yf
import pandas as pd
import requests
import numpy as np
import logging

logger = logging.getLogger()
logging.basicConfig(
    filename="logfile.log",
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M"
    )

"""
Denna filen användes bara för att bygga upp början av databasen.
Och kommer då inte kommenteras eller testas eftersom den inte skall vara med i den Schemalaggda delen.
Man får självklart läsa igenom koden. eventuella egna kommentarer finns
"""


class Get_sp500_list:
    def __init__(self) -> None:
        self.url = ("https://www.wikitable2json.com/api/List_of_S%26P_500_companies?table=0")
        
             
    def request_to_pd(self):
        self.data = requests.get(self.url).json() 
        df = pd.DataFrame(columns = self.data[0][0])
        for i in range(len(self.data[0])-1):
            df.loc[len(df)] = self.data[0][i+1]
        self.df = df
        self.df["Earnings date"] = np.nan
        self.df["Symbol"] = self.df["Symbol"].str.replace(".","-")
        
    
        
    def get_earnings_date(self):
        self.df["Last update"] = "1900-01-01"
        for i in range(len(self.df)):
            try:
                ticker = yf.Ticker(self.df["Symbol"][i])
                if len(ticker.calendar["Earnings Date"]) >= 1:
                    earning_date = ticker.calendar["Earnings Date"][0]
                else:
                    earning_date = None 
                    logger.warning("No earnings date was found for "+ self.df["Symbol"][i]+ ", Date is set as None")
            except Exception as e:
                print(e)
                logging.warning(e)
                logging.warning("at "+ i)    
            self.df.at[i, "Earnings date"] = earning_date
                   
    """
    Notering, sparad log säger att vi fick 404 client error. samt en warning vid no earnings found hos BRK.B
    BRK.B är ett stortföretag som skall har en earnings date. vi kontroll så uppmärks det att yahoo finance
    har bytt ut punkt "." till bindes streck "-"
    Error förekommer när vi försöker nå data från BF.B som försöker då nå en url hos .calendar som inte existerar
    vilket krasha programmet.
    
    uppfölj: byt ut . mot -, byte görs nu i request_to_pd() metoden
    """        
            
    def get_df(self):
        return self.df