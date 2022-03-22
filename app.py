from flask import Flask, url_for, redirect, request, render_template
from flask_pymongo import PyMongo

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
    return render_template("menu.html")