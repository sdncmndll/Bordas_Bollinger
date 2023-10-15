import yfinance as yf
import datetime

def get(ticker:str, init_date: datetime = None, end_date: datetime = None):
    
    stock= yf.Ticker(ticker +'.SA')

    hist = stock.history(period="max")

    init_date = str(init_date) #+ "00:00:00-03:00"
    end_date = str(end_date) #+ "00:00:00-03:00"

    hist = hist.loc[(hist.index >= init_date) & (hist.index <= end_date)]

    df=hist[["Open","Close","High","Low","Dividends"]]
    df.insert(5,'Moving Average', df["Close"].rolling(window=20).mean(),allow_duplicates=False)
    df.insert(6,'Standart Deviation', df["Close"].rolling(window=20).std(),allow_duplicates=False)
    df = df.dropna(axis=0, inplace=False)
    df.insert(7,'Upper Band', df["Moving Average"]+(df["Standart Deviation"]*2),allow_duplicates=False)
    df.insert(8,'Lower Band', df["Moving Average"]-(df["Standart Deviation"]*2),allow_duplicates=False)
    df.insert(9,'Purchase', df["Close"][df["Close"] >= df["Upper Band"]],allow_duplicates=False)
    df.insert(10,'Sell', df["Close"][df["Close"] <= df["Lower Band"]],allow_duplicates=False)

    return ([df, stock])