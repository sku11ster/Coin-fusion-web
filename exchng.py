from flask import Flask, render_template
import requests
import hmac
import hashlib

def binance_signature(query_params, secret_key):
    query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

import requests

@app.route('/exchange')
def exchange():
    # retrieve list of available cryptocurrencies
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params={
        'vs_currency': 'usd',
        'per_page': 100,
        'order': 'market_cap_desc'
    })
    if response.status_code == 200:
        cryptocurrencies = [currency['symbol'].upper() for currency in response.json()]
        cryptocurrency_data = {currency['symbol'].upper(): {'name': currency['name'], 'price': currency['current_price']} for currency in response.json()}
    else:
        # if the API request fails, return an error message
        return 'Error retrieving cryptocurrency data'
    
    # return exchange template with cryptocurrency data
    return render_template('exchange.html', cryptocurrencies=cryptocurrencies, cryptocurrency_data=cryptocurrency_data)

@app.route('/exchange/<pair>')
def exchange_pair(pair):
    # retrieve order book data for specified cryptocurrency pair
    response = requests.get('https://api.binance.com/api/v3/depth', params={
        'symbol': pair.upper(),
        'limit': 20
    })
    if response.status_code == 200:
        order_book_data = {'bids': response.json()['bids'], 'asks': response.json()['asks']}
    else:
        # if the API request fails, return an error message
        return 'Error retrieving order book data'
    
    # return exchange pair template with order book data
    return render_template('exchange_pair.html', pair=pair.upper(), order_book=order_book_data)

@app.route('/wallet')
def wallet():
    wallet_data = {}
    total_balance = sum(wallet_data.values())
    return render_template('wallet.html', wallet=wallet_data, total_balance=total_balance)

@app.route('/buy')
def buy():
    available_currencies = ['BTC', 'ETH', 'ZEN', 'GMT']
    
    # retrieve real-time prices for the available cryptocurrencies
    response = requests.get('https://api.coingecko.com/api/v3/simple/price', params={
        'ids': ','.join(available_currencies),
        'vs_currencies': 'usd'
    })
    if response.status_code == 200:
        prices = {currency.upper(): response.json()[currency]['usd'] for currency in available_currencies}
    else:
        # if the API request fails, return an error message
        return 'Error retrieving cryptocurrency prices'
    
    return render_template('buy.html', currencies=available_currencies, prices=prices)

@app.route('/sell')
def sell():
    available_currencies = ['BTC', 'ETH', 'ZEN', 'GMT']  
    
    # retrieve real-time prices for the available cryptocurrencies
    response = requests.get('https://api.coingecko.com/api/v3/simple/price', params={
        'ids': ','.join(available_currencies),
        'vs_currencies': 'usd'
    })
    if response.status_code == 200:
        prices = {currency.upper(): response.json()[currency]['usd'] for currency in available_currencies}
    else:
        # if the API request fails, return an error message
        return 'Error retrieving cryptocurrency prices'
    
    # retrieve user's wallet balances from Binance API
    api_key = 'your_binance_api_key'
    api_secret = 'your_binance_api_secret'
    response = requests.get('https://api.binance.com/api/v3/account', params={
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000,
        'signature': binance_signature({'timestamp': int(time.time() * 1000)}, api_secret)
    }, headers={
        'X-MBX-APIKEY': api_key
    })
    if response.status_code == 200:
        wallet_data = {asset['asset']: float(asset['free']) for asset in response.json()['balances']}
    else:
        # if the API request fails, return an error message
        return 'Error retrieving wallet balances'
    
    # determine which cryptocurrencies are sellable based on user's wallet balances
    sellable_currencies = {}
    for currency in available_currencies:
        if currency in wallet_data and wallet_data[currency] > 0:
            sellable_currencies[currency] = wallet_data[currency]
    
    return render_template('sell.html', currencies=sellable_currencies, prices=prices)
