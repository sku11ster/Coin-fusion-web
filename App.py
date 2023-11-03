from flask import Flask, render_template, request, make_response,session,redirect,url_for

from datetime import datetime, date
import requests

from getprice import get_price_in_usdt



app = Flask(__name__)
app.secret_key = 'my_secret_key'

server = '.'
database = 'proj'
driver = '{SQL Server}'


conn_str = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    Trusted_Connection=yes;
"""

conn = pyodbc.connect(conn_str)




    
    
#  @app.route('/login',methods=["GET","POST"])

#  def converter():
#     session=db.session()

#     currency_from='USDT'
#     currency_to='BUSD'
#     ammount=5
#     response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={currency_from}&vs_currencies={currency_to}")
#     if response.status_code==200:
     
#      try:

#         conversion_rate = response.json()[currency_from][currency_to]
#         converted_ammount=ammount*conversion_rate
#         keyword='e'
#      except keyword as e:
#         return 'nigga error'

#         wallet=session.query(Wallet).filter_by(Wallet_Id='1',User_Id='1',Currency_code=currency_from).first()
#         if wallet is true :
#             wallet.Balance+=converted_ammount
#             wallet.Currency_code=currency_to
#             wallet.Last_update=datetime.utnow()
#             session.commit()
#         else:
#             return render_template('post.html')


@app.route("/")
def great():
    return render_template("index.html")




@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["GET","POST"])
def signupform():
   
         name = request.form.get('txt')
         email = request.form.get('email')
         password = request.form.get('pswd')
         action=request.form.get('action')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM Users WHERE name = ? AND email = ?", (name, email))
         rows = cursor.fetchall()
         if rows:
           
            error = "User already exists!"
            return "User Already Exist!"
         else:
            u_timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            w_timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')


            user_id = f"{name}-{u_timestamp}"
            wallet_id = f"{w_timestamp}"
            
            cursor.execute("insert into Wallet(Wallet_Id) values( '"+wallet_id+"');INSERT INTO Users (User_ID, Name, Email, Password,Wallet_Id) VALUES (?, ?, ?, ?,?)", (user_id, name, email, password,wallet_id))
            conn.commit()
           
            return render_template("signup.html")
         
       
    
@app.route("/login", methods=["GET","POST"])
def loginform():
    cursor=conn.cursor()
    email = request.form.get('log_email')
    password = request.form.get('log_pswd')
    cursor.execute("SELECT * FROM Users WHERE Password = ? AND Email = ?", (password, email))
    rows = cursor.fetchall()
    if rows:
        check_email=rows[0][2]
        check_pass=rows[0][3]
        user_id=rows[0][0]
        wallet_id=rows[0][4]
        session['User_Id']=user_id
        session['Wallet_Id']=wallet_id
        conn.commit()
        return redirect(url_for('dashboard'))
    else :
        conn.commit()
        return "Login failed"
    



@app.route('/dashboard')
def dashboard():
    
    cursor=conn.cursor()
    User_Id=session["User_Id"]
    cursor.execute("Select Wallet_Id from Users where User_Id='"+User_Id+"'")
    
    row1=cursor.fetchall()
    wallet_id=row1[0][0]

    dollar='usdt'
    cursor.execute("Select sum(Balance) from Wallet where Wallet_Id='"+wallet_id+"' and Currency_code=?",(dollar))
    row2=cursor.fetchall()
    if row2:
     Balance_dollar=row2[0][0]
    else:
        Balance_dollar=0.0
    


    btc='btc'
    currency=[]
    total_usdt=0
    total_btc=0
    cursor.execute("Select Balance,Currency_code from Wallet where Wallet_Id=?",(wallet_id))
    row3=cursor.fetchall()
    if row3:
        i=0
        for i in range(len(row3)):
            if row3[i][1]=='usdt':
                total_usdt=total_usdt+row3[i][0]
            else:
               get = str(row3[i][1])
               get = get.upper()
               price=get_price_in_usdt(currency,get)
               total_usdt=total_usdt+price
        
        one_btc=get_price_in_usdt('BTC',1)
        one_btc = float(one_btc)
        total_btc=total_usdt/one_btc



    else:
        total_btc=0.0
        total_usdt=0.0
    
    conn.commit()

    return render_template('dashboard.html',port_val=total_usdt,port_val_btc=total_btc)



@app.route('/buy')
def buy():
    return render_template('/buy.html')

@app.route('/submit',methods=["GET","POST"])
def bought():
    cursor=conn.cursor()


    u_timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    deposit_id = f"{u_timestamp}"
    
    User_Id=session['User_Id']
    Wallet_id=session['Wallet_Id']
    card_name=request.form.get('card-name')
    card_num=request.form.get('card-number')
    exp_date=request.form.get('expiry-date')
    cvv=request.form.get('cvv')
    amount=request.form.get('usdt-amount')
    datenow=datetime.now().date().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO Deposit (Deposit_Id, User_Id, Wallet_Id, Card_Name, Card_Num, Ammount, Currency, CVV, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (deposit_id, User_Id, Wallet_id, card_name, card_num, amount, 'usdt', cvv, datenow))
    
    cursor.execute('select * from Wallet where Wallet_Id=? and Currency_code=?',(Wallet_id,"usdt"))
    row=cursor.fetchall()
    if not row:
        cursor.execute('insert into Wallet(Wallet_Id,Currency_code) values(?,?)',(Wallet_id,'usdt'))

    cursor.execute('update wallet set Balance=Balance+? where Wallet_Id=? and Currency_code=?',(amount,Wallet_id,"usdt"))
    cursor.execute('insert into transactions(Transaction_Id,Wallet_Id_from,Wallet_Id_to,Price,Currency,date,Type) values(?,?,?,?,?,?,?)',(deposit_id,'NULL Address',Wallet_id,amount,'usdt',datenow,'Bought'))
    conn.commit()


    return redirect(url_for('dashboard'))



    
    
@app.route('/converter')
def converter():
    return
     




if __name__== '__main__':
    app.run(debug=True)
    
    





