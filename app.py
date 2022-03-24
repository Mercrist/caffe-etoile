from flask import Flask, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
from Classes.Statics import menu as cafe_menu
from Classes.Statics import MenuItem

app = Flask(__name__) #initialize flask app

# Enter MongoDB Details into Flask's config file
# and initialize the DB. Collections are created once.
# Access collection via db.collection_name
app.config.from_object('config') 

mongo = PyMongo(app)
db = mongo.db
db.create_collection('menu')

'--Routes--'
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/menu')
def menu():
    return render_template("menu.html",
    coffees = db.menu.find({"category": "Coffee"}),
    sandwiches = db.menu.find({"category": "Sandwiches"}),
    pastries = db.menu.find({"category": "Pastries"}),
    desserts = db.menu.find({"category": "Desserts"}),
    specialties = db.menu.find({"category": "Specialty"}))