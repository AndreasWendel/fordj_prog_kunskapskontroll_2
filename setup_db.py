import sqlite3
#import sp500_list_getter
import pandas as pd


"""
sp500 = sp500_list_getter.GetSp500List()
sp500.request_to_pd()
sp500.get_earnings_date()
sp500_df = sp500.get_df()

notera så här kan man skapa den direkt från klassen 
men eftersom vi redan har sparat en csv fil från create_sp500_list.py så använder vi den
så slipper vi köra onödiga request.
"""

path = "kunskapskontroll_2/"
#ändra path efter behov/vart data är nerladdad.
#om du kör programmet själv så kan du använda koden som är docstringad

sp500 = pd.read_csv(path+"data.csv")

conn = sqlite3.connect(path+"Stock Database.db")
#note database will be created if not found/existing

sp500.to_sql("SP500", conn, if_exists="replace")

conn.close()

df = pd.read_sql_query('SELECT * FROM SP500', conn)

conn.close()