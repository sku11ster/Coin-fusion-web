from flask import Flask, render_template, redirect, url_for
import requests,json
import qrcode
import io
import base64


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/markets')
def markets():
    return render_template('markets.html')

@app.route('/deposit-withdrawal')
def deposit_withdrawal_addy():
    #hamza vro compute the crypto address here and store it in var "addy"



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
    
    

if __name__ == '__main__':
    app.run(debug=True)
