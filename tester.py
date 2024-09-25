from access_db import DBAccess
from api import API
import sqlite3
import pytest
import pandas as pd
import datetime as dt


def test_dbaccess_1(): 
    path = "" 
    db = "Stock Database.db"
    dbaccess = DBAccess(path,db)
    assert isinstance(dbaccess.conn, sqlite3.Connection) == True
    df = pd.read_sql_query('SELECT * FROM SP500', dbaccess.conn)
    assert isinstance(df, pd.DataFrame) == True
    dbaccess.close_connection()

def test_dbaccess_2():
    path = "" 
    db = "StockDatabase.db" #wrong name
    with pytest.raises(sqlite3.Error):
        dbaccess = DBAccess(path,db)
    
def test_dbaccess_3():
    path = "" 
    db = "Stock Database.db"
    dbaccess = DBAccess(path,db)
    list_ = dbaccess.check_earnings_last_update()
    assert isinstance(list_, list) == True
    assert not list_ == False #should not be empty in this case
    dbaccess.close_connection()

def test_dbaccess_4():
    path = "" 
    db = "Stock Database.db"
    dbaccess = DBAccess(path,db)
    api = API()
    test_list = ["aapl"]
    api.add_list(test_list)
    api.get_financials()
    aapl_incomestmt = api.get_list_of_df()
    assert not aapl_incomestmt == False
    assert isinstance(aapl_incomestmt[0], pd.DataFrame) == True
    failed_update = dbaccess.insert_financial_data(aapl_incomestmt)
    assert not failed_update == False
    assert failed_update[0] == "aapl"
    dbaccess.close_connection()
    

def test_api_1():
    
    api = API()
    test_list = []
    api.add_list(test_list)
    temp = api.list_of_companies
    assert isinstance(temp,list) == True
    assert not temp == True
    test_list = ["aapl"]
    api.add_list(test_list)
    temp = api.list_of_companies
    assert not temp == False
    assert temp[0] == "aapl"
   
   
def test_api_2():
    
    api = API()
    test_list = ["aapl"]
    api.add_list(test_list)
    temp = api.list_of_companies
    assert isinstance(temp,list) == True
    assert not temp == False
    api.get_financials()
    df = api.get_earnings_date()
    assert isinstance(df, pd.DataFrame) == True
    assert df.empty == False
    list_df, list_failed, time = api.get_all()
    assert isinstance(time, dt.datetime) == False
    assert isinstance(time, str) == True
    assert not list_failed == True
    assert not list_df == False
    assert len(list_df) == 1
    assert list_df[0].empty == False
    
    

#pytest -o log_cli=true tester.py