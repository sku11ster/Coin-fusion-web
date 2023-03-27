from flask import Flask, render_template, request
import requests,json
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
def deposit_withdrawal():
    return render_template('deposit-withdrawal.html')


if __name__ == '__main__':
    app.run(debug=True)
