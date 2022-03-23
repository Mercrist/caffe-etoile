from flask import Flask, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
from Classes.Statics import menu as cafe_menu
from Classes.Statics import MenuItem

app = Flask(__name__) #initialize flask app

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
    coffees=[item for item in cafe_menu.values() if item.category == "Coffee"],
    sandwiches=[item for item in cafe_menu.values() if item.category == "Sandwiches"],
    pastries=[item for item in cafe_menu.values() if item.category == "Pastries"],
    desserts=[item for item in cafe_menu.values() if item.category == "Desserts"],
    specialties=[item for item in cafe_menu.values() if item.category == "Specialty"])