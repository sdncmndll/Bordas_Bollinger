import yfinance as yf
import datetime
#Função para pegar os dados das ações e retornar em um dataframe pandas
def get(ticker:str, init_date: datetime = None, end_date: datetime = None):
    #Parâmentros da consulta
    stock= yf.Ticker(ticker +'.SA')
    init_date = str(init_date) #+ "00:00:00-03:00"
    end_date = str(end_date) #+ "00:00:00-03:00"

    #Traz todos os dados sem filtros
    hist = stock.history(period="max")

    #Filtrando o dataset
    hist = hist.loc[(hist.index >= init_date) & (hist.index <= end_date)]

    #Traz as informações da biblioteca e agraga colunas calculadas 
    df=hist[["Open","Close","High","Low","Dividends"]]
    #Faz o cálculo da média móvel em uma janela deslizante de 20 dias e coloca em uma coluna do df
    df.insert(5,'Moving Average', df["Close"].rolling(window=20).mean(),allow_duplicates=False)
    #Faz o cálculo do desvio padrão em uma janela deslizante de 20 dias e coloca em uma coluna do df
    df.insert(6,'Standart Deviation', df["Close"].rolling(window=20).std(),allow_duplicates=False)
    df = df.dropna(axis=0, inplace=False)
    df.insert(7,'Upper Band', df["Moving Average"]+(df["Standart Deviation"]*2),allow_duplicates=False)
    df.insert(8,'Lower Band', df["Moving Average"]-(df["Standart Deviation"]*2),allow_duplicates=False)
    df.insert(9,'Purchase', df["Close"][df["Close"] >= df["Upper Band"]],allow_duplicates=False)
    df.insert(10,'Sell', df["Close"][df["Close"] <= df["Lower Band"]],allow_duplicates=False)

    #Retorna o dataset e a instância da biblioteca das ações
    return ([df, stock])