from flask import Flask, url_for, redirect, request, render_template, make_response, Response, session, flash
from flask_pymongo import PyMongo
from Classes import Statics as local_data
from Classes.Shopping import ShoppingCart as ShoppingCart
from model import json_to_cart

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
        local_data.reset_menu_collection()

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
    return render_template("menu.html", database = db, categories=local_data.categories)

@app.route("/order",methods=['GET','POST'])
def order():
    if "cart" not in session:
        flash("There's in nothing your cart!")
        session['cart'] = vars(ShoppingCart("User"))

    return render_template("order.html", cart=session['cart'])

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       pass

@app.route('/add_to_cart/<string:item_name>',methods=['POST'])
def add_to_cart(item_name):
    if 'cart' not in session:
        print('CART NOT FOUND')
        session['cart'] = vars(ShoppingCart("User"))

    print(session['cart'])
    cart = json_to_cart(session['cart'])
    print(cart)
    cart.add_items(item_name)
    session.pop('cart')
    session['cart'] = vars(cart)
    session.modified = True
    print("added to cart!")
    print(session['cart'])

    return redirect("/menu")

# #background process happening without any refreshing
# @app.route('/background_process_test')
# def background_process_test():
#     print ("Attempted to add item")
#     print(request.data)
#     if "cart" not in session:
#         session['cart'] = ShoppingCart("User")
    
#     session['cart'].add_item()

#     return ("nothing")
