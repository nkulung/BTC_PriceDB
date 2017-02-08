import requests
import urllib3
from bs4 import BeautifulSoup as bs
import sqlite3
import datetime


conn = sqlite3.connect('BTC_Manager.db',detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS BTC_Price(Datestamp DATE, Price REAL)')

def getPrice():
    s = requests.get('https://www.coinbase.com/charts').text
    soup = bs(s,"html.parser")
    btcPrice = soup.find("li", {"class": "top-balance"})
    btcPriceRaw = btcPrice.text
    btcPriceInt = btcPriceRaw.split()
    btcPriceInt = btcPriceInt[3].replace("$","")
    try:
        btcPriceFloat = float(btcPriceInt)
    except ValueError:
        btcPriceInt = btcPriceInt.replace(",","")
        btcPriceFloat = float(btcPriceInt)
    return btcPriceFloat

def appendData(btcPriceFloat):
    now = datetime.datetime.now()
    date = now.strftime("%m-%d-%Y %H:%M")
    c.execute("INSERT INTO BTC_Price(Datestamp,Price) VALUES (?,?)",(date,btcPriceFloat,))
    conn.commit()
    conn.close()



def main():
    createTable()
    price = getPrice()
    appendData(price)

main()

    
    
