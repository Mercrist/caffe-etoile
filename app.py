from flask import Flask, url_for, redirect, request, render_template, make_response, Response, session, flash
from flask_pymongo import PyMongo
from Classes import Statics as local_data
from Classes.Shopping import ShoppingCart as ShoppingCart
from Classes.Shopping import Receipt
from model import json_to_cart, receipt_to_json
import json

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
    if request.args.get('checked_out'):
        receipt_number = request.args.get('receipt')
        print(receipt_number)
        print(type(receipt_number))

        receipt = db.receipts.find_one({"receipt_number":receipt_number})
        print(receipt)
        print(type(receipt))

        return render_template("menu.html", 
            database=db, 
            categories=local_data.categories,
            checked_out=True,
            receipt=receipt)
    return render_template("menu.html", 
        database = db,
        categories=local_data.categories, 
        checked_out=False)

@app.route("/order",methods=['GET','POST'])
def order():
    if "cart" not in session:
        flash("There's in nothing your cart!")
        session['cart'] = vars(ShoppingCart("User"))

    return render_template("order.html", cart=session['cart'])

@app.route('/add_to_cart/<string:item_name>',methods=['POST'])
def add_to_cart(item_name):
    if 'cart' not in session:
        print('CART NOT FOUND')
        session['cart'] = vars(ShoppingCart("User"))

    amount = int(request.form['amount'])
    print(session['cart'])
    cart = json_to_cart(session['cart'])
    print(cart)
    cart.add_items(item_name,amount)
    session.pop('cart')
    session['cart'] = vars(cart)
    session.modified = True
    print("added to cart!")
    print(session['cart'])

    return redirect("/menu")

@app.route('/checkout',methods=["POST"])
def checkout():
    print(request.form)
    cart = json_to_cart(session['cart']) 
    if request.form['firstName']:
        cart.name = request.form['firstName']
    if request.form['reservationDay'] and request.form['reservationHour'] and request.form['reservationMeridiem']:
        day = request.form['reservationDay']
        hour = request.form['reservationHour']
        meridiem = request.form['reservationMeridiem']
        cart.set_reservation(day,hour,meridiem)
        print(cart)

    receipt = Receipt(cart.cart,cart.reservation,cart.name,cart.subtotal)
    print(receipt)
    if 'receipts' not in db.list_collection_names():
        db.create_collection('receipts')
    json_receipt = receipt_to_json(receipt)
    db.receipts.insert_one(json_receipt) 
    print([receipt for receipt in db.receipts.find({})])
    if request.form.get('downloadReceipt'):
        receipt.generate_receipt()

    #clear out cart "cache"
    session.pop('cart')
    return redirect(url_for("menu",checked_out=True,receipt=json_receipt['receipt_number']))

