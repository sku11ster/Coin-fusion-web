from flask import Flask, render_template, request
import requests,json
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')


if __name__ == '__main__':
    app.run(debug=True)
