from flask import Flask, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
import model

app = Flask(__name__) #initialize flask app

# Enter MongoDB Details into Flask's config file
# and initialize the DB. Collections are created once.
# Access collection via db.collection_name
app.config.from_object('config') 

mongo = PyMongo(app)
db = mongo.db
# first time setup
if 'menu' not in db.list_collection_names():
    db.create_collection('menu')
    # passes flask as context to this function
    # in order to access the MongoDB URI
    with app.app_context():
        model.reset_menu_collection()

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
    return render_template("menu.html", database = db, categories=model.categories)