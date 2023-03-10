from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://./se proj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class Users(db.Model):
    __tablename__ = 'Users'
    User_Id = db.Column(db.String(50), primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50))
    Password = db.Column(db.String(50))
    Wallet_Id = db.Column(db.String(100))
    Date_of_birth = db.Column(db.Date)

    def __init__(self, User_Id, Name, Email, Password, Wallet_Id, Date_of_birth):
        self.User_Id = User_Id
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.Wallet_Id = Wallet_Id
        self.Date_of_birth = Date_of_birth

    
    


@app.route("/")
def great():
    name = 'Hamza'
    return render_template("login.html", name=name)




@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signupform():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()  # convert the string to a date object
        user_id = str(datetime.now().timestamp())  # generate a unique user id
        wallet_id = str(datetime.now().timestamp())  # generate a unique wallet id
        user = Users(user_id, name, email, password, wallet_id, dob)
        db.session.add(user)
        db.session.commit()


    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
  
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(Email=email).first()
        
        if user is not None  and user.Password == password:
            return render_template("exchange.html")
    
    
if __name__== '__main__':
    app.run(debug=True)
    
    





