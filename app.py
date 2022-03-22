from flask import Flask, url_for, redirect, request, render_template
import pymongo

app = Flask(__name__) #initialize flask app

'--Routes--'
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return "Placeholder"

@app.route('/contact')
def contact():
    return "Placeholder"

@app.route('/menu')
def menu():
    return "Placeholder"