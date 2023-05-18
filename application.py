from flask import Flask,request,render_template, redirect, url_for, jsonify,abort
import requests,json
import qrcode
import io
import base64
import datetime
import json
import ccxt
import talib
import plotly.graph_objs as go
from binance.client import Client
from datetime import datetime, timedelta
import numpy as np




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    #Do processing here to pass assets info to frontend
    assets='hellow'
    return render_template('dashboard.html',assets=assets)

@app.route('/settings')
def settings():
    return render_template('userprofile.html')

@app.route('/update', methods=['POST'])
def update():
    update_option = request.form['update_option']

    if update_option == 'email':
        email = request.form['email']
        # Process and update the email
        # ...

        message = f'Email updated to: {email}'
    else:
        password = request.form['password']
        # Process and update the password
        # ...

        message = 'Password updated'

    return message

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/deposit-withdrawal')
def deposit_withdrawal_addy():
    #hamza vro compute the crypto address here and store it in var "addy"
    addy='0x1213124151'

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data("address:" + addy)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to a base64-encoded string and embed it in the HTML
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    qr_src = f"data:image/png;base64,{img_str}"

    return render_template('deposit-withdrawal.html', address=addy, qr_src=qr_src)



@app.route('/withdraw', methods=['POST'])
def withdraw():
    coin_id = request.form['coin']
    amount = float(request.form['amount'])
    address = request.form['address']
    return 'Withdrawal successful'
    


@app.route('/markets',methods=['POST','GET'])
def market():
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    data = response.json()
    usdt_pairs = [d for d in data if d['symbol'].endswith('USDT')]
    top_200 = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)[:200]
    
    query = request.args.get('q')
    if query:
        top_200 = [coin for coin in top_200 if query.lower() in coin['symbol'].lower()]
        
    return render_template('markets.html', top_200=top_200, query=query)

#For Trading

@app.route('/trade/<pair>', methods=['GET', 'POST'])
def trade(pair):
    interval = request.args.get('interval', '4h') # replace with desired timeframe interval
    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}"
    response = requests.get(url)
    data = response.json()

    x_values = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []
    candle_text = []

    for d in data:
        timestamp = int(d[0])/1000
        x_values.append(datetime.fromtimestamp(timestamp))
        open_values.append(float(d[1]))
        high_values.append(float(d[2]))
        low_values.append(float(d[3]))
        close_values.append(float(d[4]))
        candle_text.append(f"Open: {d[1]}<br>High: {d[2]}<br>Low: {d[3]}<br>Close: {d[4]}")

    trace_candlestick = go.Candlestick(x=x_values,
                                       open=open_values,
                                       high=high_values,
                                       low=low_values,
                                       close=close_values,
                                       name='Candlestick',
                                       text=candle_text,
                                       hoverinfo='text')

    rsi_values = talib.RSI(np.array(close_values), timeperiod=14)

    trace_rsi = go.Scatter(x=x_values,
                       y=rsi_values,
                       name='RSI',
                       yaxis='y2')  # Set visibility to 'legendonly'



    # add trace_rsi in the data list to show the rsi line

    volume_values = [float(d[5]) for d in data]

    color_values = ['green' if close > open else 'red' for close, open in zip(close_values, open_values)]

    trace_volume = go.Bar(
    x=x_values,
    y=volume_values,
    name='Volume',
    yaxis='y3',
    marker=dict(color=color_values),
    opacity=1)

    data = [trace_candlestick, trace_volume]


    layout = go.Layout(
    title=f"{pair} Candlestick Chart ({interval})",
    xaxis=dict(
        type='date',
        showgrid=False,  # Remove x-axis gridlines
        zeroline=False,  # Remove the white line on the x-axis
    ),
    yaxis=dict(fixedrange=False, showgrid=False),  # Remove y-axis gridlines and enable range selection
    yaxis2=dict(fixedrange=True, showgrid=False, overlaying='y', side='right'),  # RSI axis
    xaxis2=dict(anchor='y2', showgrid=False),  # RSI x-axis
    yaxis3=dict(fixedrange=True, showgrid=False, overlaying='y', side='right'),  # Volume axis

    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    hoverdistance=-1,
    spikedistance=-1,
    width=900,  # Adjust the width of the graph (in pixels)
    height=450,  # Adjust the height of the graph (in pixels)
    margin=dict(t=40, b=40, r=40, l=40),  # Adjust the margins
    showlegend=False,  # Hide the legend
    dragmode='pan',  # Enable chart dragging
    uirevision='true',  # Preserve zoom/pan state during updates
    shapes=[dict(type='rect', xref='paper', yref='paper', x0=0, y0=0, x1=1, y1=1, fillcolor='rgba(0,0,0,0)', layer='below', line=dict(color='rgba(0,0,0,0)'))],  # Transparent overlay to capture events outside the chart area
)

    fig = go.Figure(data=data, layout=layout)

    total = 0.0  # Assign a default value to total

    if request.method == 'POST':
        order_type = request.form.get('order_type')
        quantity = float(request.form.get('quantity'))
        price = float(request.form.get('price'))

        if order_type == 'buy':
            # Perform buy order logic
            total = quantity * price
            print(total)
            print(quantity)
            print(price)
            # Implement buy order processing here...

        elif order_type == 'sell':
            # Perform sell order logic
            total = quantity * price
            print(total)
            print(quantity)
            print(price)
            # Implement sell order processing here...

        return render_template('trades.html', chart=fig.to_html(full_html=False), order_type=order_type, quantity=quantity, price=price, total=total)

    # Default values for order_type when it's not a POST request
    order_type = None
    quantity = None
    price = None
    total = None

    return render_template('trades.html', chart=fig.to_html(full_html=False), order_type=order_type, quantity=quantity, price=price, total=total)


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    # Retrieve portfolio data from DB

    return render_template('portfolio.html')


#Api for updating date and time
@app.route('/nft')
def nft():

    return render_template('nft.html')


#Api for updating date and time
@app.route('/datetime')
def get_datetime():
    now = datetime.now()
    date = now.strftime("%d") 
    time = now.strftime("%H:%M")
    return {'date': date, 'time': time}


@app.route('/pie-data')
def pie_data():
    asset=['btc','ltc','eth','pepe','luna','rndr']
    total_amount=['26000','2000','2500','12000','2000','9870']
    return {'asset_name': asset, 'total_amount': total_amount}


@app.route('/port-history')
def port_history():
    month=['jan','feb','mar','apr','may','june','july','aug']
    port_worth=['26000','2000','2500','12000','2000','10000','10','999']
    return {'month_names': month, 'port_val': port_worth}



# Endpoint to retrieve user balance
@app.route('/user-balance', methods=['GET'])
def get_user_balance():
    # Replace with your logic to fetch user balance from database or storage
    balance = 1000
    return jsonify({'balance': balance})

# Endpoint to update user balance
@app.route('/user-balance', methods=['POST'])
def update_user_balance():
    # Retrieve the new balance from the request body
    new_balance = request.json.get('balance')

    # Replace with your logic to update the user balance in the database or storage
    # Here, we are simply returning a success response
    return jsonify({'success': True})

# Endpoint to add NFT to user's assets
@app.route('/add-nft', methods=['POST'])
def add_nft_to_assets():
    # Replace with your logic to add the NFT to the user's assets
    # Here, we are simply returning a success response
    return jsonify({'success': True})

# Endpoint to remove NFT from sale
@app.route('/remove-nft', methods=['POST'])
def remove_nft_from_sale():
    # Replace with your logic to remove the NFT from sale
    # Here, we are simply returning a success response
    return jsonify({'success': True})



@app.route('/nft/marketplace')
def marketplace():
    return render_template('nft-marketplace.html')



# Sample NFT data
nfts = [
    {"id": 1, "image": "https://i.seadn.io/gae/71Pizh-IAOmg76IbOyTrdoNrpRyqszDyHLM5CK8xbt1NNYvbmPHefXZn9QXE6FyG-z5CgNK2WzRfMFvnGib-gVqpkYlSdLJEmW6Sskg?auto=format&dpr=1&w=1920", "price": 10},
    {"id": 2, "image": "https://i.seadn.io/gcs/files/5dfa09c912238b09224b88459a74998c.png?auto=format&dpr=1&w=1000", "price": 200},
    {"id": 3, "image": "https://i.seadn.io/gcs/files/1363e4c8f6fbfcc1c81b28fc91c3a768.png?auto=format&dpr=1&w=1000", "price": 300},
    {"id": 4, "image": "https://i.seadn.io/gcs/files/fffaa224da5ac2df363d54da7bb9cd52.png?auto=format&dpr=1&w=1000", "price": 400},
    {"id": 5, "image": "https://i.seadn.io/gae/MuMkztXxQZ3Z-wh8GSXUHk79PjQbtmagpM4Gu89FXCdR0EhinboxYKQ1KR_XCkNqgV_RMpi3Ctr1FpySjbhKuVIAEx2aELUvz8iX2JA?auto=format&dpr=1&w=1000", "price": 320},
    {"id": 6, "image": "https://i.seadn.io/gae/f-gSODCsZDW6aQ72KJpRnWohjhH4HKw7fz-43nKn_yhrH77hWeeaJi-VlTKRWlBLQTyhBBjVqXtqY0MadWcWSSSAsjukpMaa3FUHOw?auto=format&dpr=1&w=1920", "price": 500},
    {"id": 7, "image": "https://i.seadn.io/gcs/files/1363e4c8f6fbfcc1c81b28fc91c3a768.png?auto=format&dpr=1&w=1000", "price": 300},
    {"id": 8, "image": "https://i.seadn.io/gae/71Pizh-IAOmg76IbOyTrdoNrpRyqszDyHLM5CK8xbt1NNYvbmPHefXZn9QXE6FyG-z5CgNK2WzRfMFvnGib-gVqpkYlSdLJEmW6Sskg?auto=format&dpr=1&w=1920", "price": 10},
    {"id": 9, "image": "https://i.seadn.io/gcs/files/5dfa09c912238b09224b88459a74998c.png?auto=format&dpr=1&w=1000", "price": 200},
    {"id": 10, "image": "https://i.seadn.io/gcs/files/1363e4c8f6fbfcc1c81b28fc91c3a768.png?auto=format&dpr=1&w=1000", "price": 300},
    {"id": 11, "image": "https://i.seadn.io/gcs/files/fffaa224da5ac2df363d54da7bb9cd52.png?auto=format&dpr=1&w=1000", "price": 400},
    {"id": 12, "image": "https://i.seadn.io/gae/MuMkztXxQZ3Z-wh8GSXUHk79PjQbtmagpM4Gu89FXCdR0EhinboxYKQ1KR_XCkNqgV_RMpi3Ctr1FpySjbhKuVIAEx2aELUvz8iX2JA?auto=format&dpr=1&w=1000", "price": 320},
    {"id": 13, "image": "https://i.seadn.io/gae/f-gSODCsZDW6aQ72KJpRnWohjhH4HKw7fz-43nKn_yhrH77hWeeaJi-VlTKRWlBLQTyhBBjVqXtqY0MadWcWSSSAsjukpMaa3FUHOw?auto=format&dpr=1&w=1920", "price": 500},
    {"id": 14, "image": "https://i.seadn.io/gcs/files/1363e4c8f6fbfcc1c81b28fc91c3a768.png?auto=format&dpr=1&w=1000", "price": 300},
    
    
]





@app.route('/nft-info')
def get_nft_info():
    return jsonify(nfts)

@app.route('/purchase')
def purchase_confirmation():
    # Perform purchase confirmation logic here
    # Calculate remaining balance, handle purchase confirmation, etc.
    remaining_balance = 80

    return render_template('purchase.html', balance=remaining_balance)


if __name__ == '__main__':
    app.run(debug=True)







if 5000 == '__main__':
    app.run(debug=True,port=5000)