from flask import Flask,redirect,render_template,request
import requests



def get_price_in_usdt(currency,price):
    currency='BTC'+'USDT'
    url = "https://api.binance.com/api/v3/ticker/price?symbol="+currency
    response = requests.get(url)
    data = response.json()
    btc_price = data['price']
    
    result=price*btc_price

    return result