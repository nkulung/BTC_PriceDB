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
    price = ''
    s = requests.get('https://www.worldcoinindex.com/coin/bitcoin').text
    soup = bs(s,"html.parser")
    btcPrice = soup.find("td", {"class" : "coinprice"})
    btcString = btcPrice.getText()
    for h in btcString:
        if(h.isdigit()):
            price += h
    num = price[:-2]
    dec = price[-2:]
    string = num + '.' + dec
    try:
        price = float(string)
    except ValueError:
        print("Price could not be retrieved")
    return price

def appendData(btcPriceFloat):
    if(btcPriceFloat == 0):
        print("Price not found")
    now = datetime.datetime.now()
    date = now.strftime("%m-%d-%Y %H:%M")
    c.execute("INSERT INTO BTC_Price(Datestamp,Price) VALUES (?,?)",(date,btcPriceFloat,))
    conn.commit()
    conn.close()
    return btcPriceFloat, date

def success(price, date):
    print('---------------------------------------')
    print("Bitcoin price: $" + str(price))
    print("Current date and time: " + date)
    print("Successfully added to the database")
    print('---------------------------------------')
    input("Press ENTER to EXIT")



def main():
    createTable()
    price = getPrice()
    price, date = appendData(price)
    success(price, date)

main()

    
    
