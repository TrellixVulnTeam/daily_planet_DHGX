from flask import Flask, render_template, request
from pymongo import *
 
app = Flask(__name__, template_folder = 'templates', static_folder = 'static')

# MongoDB Connection with PyMongo
def initDB ():
    client = MongoClient()
    db = client.daily_planet_db
    #db.create_collection("login")
    #db.create_collection("usuarios")
    #db.create_collection("articulos")
    return db

database = initDB()

# Routes Definition
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password  = request.form['password']

	return render_template('index.html')

@app.route('/pic', methods=['POST'])
def image():
	logo = request.form['to_logo']
	return render_template('logo.html', logo = logo)


if __name__ == '__main__':
	app.debug = True
	app.run()
