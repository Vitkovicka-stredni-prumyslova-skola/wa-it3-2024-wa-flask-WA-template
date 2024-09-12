from io import BytesIO #Metody potřebné pro práci se soubory
from flask import Flask, render_template, redirect, url_for, request, send_file, session
from flask_sqlalchemy import SQLAlchemy #Metody potřebné pro práci s databází
from flask_session import Session
from flask_login import LoginManager, UserMixin

from user import *

app = Flask(__name__)

#Inicializace databáze
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize app with extension
#db.init_app(app)
# Create database within app context

#with app.app_context():
#	db.create_all()

# LoginManager is needed for our application 
# to be able to log in and out users
#login_manager = LoginManager()
#login_manager.init_app(app)


#Třída pro práci s databází vytvoří tabulku o třech zmíněných sloupcích
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# Create user model
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True,
						nullable=False)
	password = db.Column(db.String(250),
						nullable=False)


#Třída pro práci s databází a produkty vytvoří tabulku o pěti zmíněných sloupcích
class UploadItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameItem = db.Column(db.String(50), )
    descriptionItem = db.Column(db.Text)
    priceItem = db.Column(db.Integer)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

#Načtení hlavní stránky
@app.route("/", methods = ["GET", "POST"])
def home():

    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}'
    
    return render_template("upload.html")

@app.route('/files')
def listOfFIles():

    listOfFiles = Upload.query.all()

    return render_template("list-of-files.html", len = len(listOfFiles), listOfFiles = listOfFiles)

#Stažení souboru do PC, který je uložený v databázi. 
@app.route('/download/<upload_id>')
def download(upload_id):
    try:
        upload = Upload.query.filter_by(id=upload_id).first()
        return send_file(BytesIO(upload.data), 
                        download_name=upload.filename, as_attachment=True)
    except :
        return f'Error: file  ID {upload_id} not found!'

#Hrátky s uživateli - vytvoření testovacích instancí objektu Uzivatel    
martin = User("Martin", None)
pepa = User("Pepa", "pepa@mail.cz")
ela = User("Ela", "ela@mail.cz")

#Pole uživatelů
users = [martin, pepa, ela]


@app.route("/contact", methods = ["GET"])
def contact():
    resultNick = request.args.get("nick")

    return render_template("index.html", uzivatel = users[0], uzivatelNick = resultNick)

#Vypsání podrobných inforamcí uživatele na základě nicku
@app.route("/contact/<nick>")
def detail_contact(nick):
    for user in users:
       
        if user.get_nick() == nick:
            return render_template("detail.html", user = user)
            break
    
    return render_template("404.html", user = nick)
 
 #Login uživatele, zatím bez hesla          
@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

# Creates a user loader callback that returns the user object given an id
#@login_manager.user_loader
#def loader_user(user_id):
#    return Users.query.get(user_id) 

#Zpracovnání a nahrání porduktu do databáze
@app.route("/upload-product", methods = ["GET", "POST"])
def upload_product():

    if request.method == 'POST':
        nameItem = request.form['nameItem']
        descriptionItem = request.form['descriptionItem']
        priceItem = request.form['priceItem']
        file = request.files['file']
        
        upload = UploadItem(nameItem, descriptionItem, priceItem, filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        
        return f'Položka vytvořena: {nameItem}'
    
    return render_template("upload-product.html")


if __name__ == '__main__':
   app.run(debug = True)