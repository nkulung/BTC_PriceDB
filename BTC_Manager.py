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
    return btcPriceFloat, date

def success(price, date):
    print('---------------------------------------')
    print("Bitcoin price: $" + str(price))
    print("Current date and time: " + date)
    print("Successfully added to the database")
    print('---------------------------------------')

def query(choice):
    if(choice == 1):
        print("CHOICE 1")
        queryByDate()
    if(choice == 2):
        print("CHOICE 2")
    if(choice == 3):
        sys.exit()
        
def queryByDate():
    while(True):
        try:
            dateRange = input("Please enter a date range (i.e. '02-02-2018, 03-02-2018'): ")
            startDate, endDate = dateRange.split(",",1)
        except ValueError:
            print("Input is invalid, format is '02-02-2018, 03-02-2018' without quotes")
            continue
        break
    startDate = startDate.lstrip(" ")
    endDate = endDate.lstrip(" ")
    startDate += " 00:00"
    endDate += " 23:59"
    startDate = datetime.datetime.strptime(startDate, "%m-%d-%Y %H:%M")
    endDate = datetime.datetime.strptime(endDate, "%m-%d-%Y %H:%M")
    currentDate = datetime.datetime.now()
    currentDate = currentDate.strftime("%m-%d-%Y %H:%M")
    print(currentDate)
    print(startDate, endDate)

    c.execute("SELECT * FROM BTC_Price  WHERE  Datestamp BETWEEN (?) AND (?)", (startDate,endDate,))
    rows = c.fetchall()
    print(rows)

    
def main():
    createTable()
    price = getPrice()
    price, date = appendData(price)
    success(price, date)
    choice = int(input("Enter 1 to query database by date, 2 to query by price, 3 to EXIT: "))
    query(choice)
    
main()

    
    
