from flask import Flask, url_for, redirect, request, render_template, make_response, Response, session, flash
from flask_pymongo import PyMongo
from Classes import Statics as local_data
from model import json_to_cart, receipt_to_json
from model import ShoppingCart, Receipt
import json
import model
import bcrypt

app = Flask(__name__) #initialize flask app

# Enter MongoDB Details into Flask's config file
# and initialize the DB. Collections are created once.
# Access collection via db.collection_name
app.config.from_object('config')

mongo = PyMongo(app)
db = mongo.db

# first time setup
for collection in model.collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)
        #resets the menu collection with
        #local menu items
        if collection == 'menu':
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
    if request.args.get('checked_out') or request.args.get('search'):
        receipt_number = request.args.get('receipt')
        print(receipt_number)
        print(type(receipt_number))

        receipt = db.receipts.find_one({"receipt_number":receipt_number})
        print(receipt)
        print(type(receipt))
        return render_template("menu.html", 
            database=db, 
            categories=model.categories,
            checked_out=True,
            receipt=receipt)
        
    if request.args.get('added'):
        flash('Added items to cart!','info')
    return render_template("menu.html", 
        database = db,
        categories=model.categories, 
        checked_out=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login' in request.form and request.form['login'] == "clicked":
            # first check if username exists
            local_username = request.form['input_username']
            login_user = db.admin.find_one({'username': local_username})
            # whether the user can log in or not
            login_attempt = True

            if not login_user:
                login_attempt = False

            # right username but wrong password
            else:
                local_pswd = request.form['input_pswd'].encode("utf-8")
                correct_pswd = bcrypt.checkpw(local_pswd, login_user['password'])

                if not correct_pswd:
                    login_attempt = False

            if not login_attempt:
                flash("Incorrect username or password.", "danger")
                return redirect(url_for('login'))

            # correctly logged into the admin page
            else:
                # prevents redirect from being interpreted as GET
                return redirect(url_for('admin', username=local_username), code=307)

    return render_template("login.html")

@app.route('/admin/<username>', methods=['GET', 'POST'])
def admin(username):
    if request.method == 'GET':
        return redirect(url_for('index'))

    # POST requests
    # add menu item button was clicked
    if 'add_item_button' in request.form and request.form['add_item_button'] == "clicked":
        new_item = {"name": request.form['item_name'], "price": round(float(request.form['item_price']), 2),
                "category": request.form['item_category'], "description": request.form['item_description'],
                "image_link": request.form['item_url']}

        # message categories: "success", "danger" (per bootstrap)
        db.menu.insert_one(new_item)
        flash(f"{new_item['name']} was added to the menu!", "success")


    elif 'remove_item_button' in request.form and request.form['remove_item_button'] == "clicked":
        item_name = request.form['remove_item_name']
        if not db.menu.find_one_and_delete({'name': item_name}):
            flash(f"{item_name} is not in the menu.", "danger")

        else:
            flash(f"{item_name} was removed from the menu!", "success")

    elif 'remove_receipt_button' in request.form and request.form['remove_receipt_button'] == "clicked":
        receipt_number = request.form['remove_receipt_number']

        if not db.receipts.find_one_and_delete({'receipt_num': receipt_number}):
            flash(f"Receipt #{receipt_number} does not exist.", "danger")

        else:
            flash(f"Receipt #{receipt_number} was removed from our logs!", "success")

    elif 'reset_menu_button' in request.form and request.form['reset_menu_button'] == "clicked":
        model.reset_menu_collection()

    elif 'reset_reservation_button' in request.form and request.form['reset_reservation_button'] == "clicked":
        model.reset_receipts_collection()

    elif 'delete_account_button' in request.form and request.form['delete_account_button'] == 'clicked':
        username_to_remove = request.form['username_to_remove']

        if username == username_to_remove:
            flash("Cannot delete the current account!", "danger")

        elif not db.admin.find_one_and_delete({'username': username_to_remove}):
            flash(f"{username_to_remove} does not exist!", "danger")

        else:
            flash("Account removed succesfully!", "success")

    elif 'new_password_button' in request.form and request.form['new_password_button'] == 'clicked':
        hashed_pswd = model.encrypt_pswd(request.form['confirm_password_input'])

        db.admin.find_one_and_update(
            {'username': username},
            {'$set': {'password': hashed_pswd}})

        flash("Password updated succesfully!", "success")

    elif 'add_account_button' in request.form and request.form['add_account_button'] == 'clicked':
        local_username = request.form['new_acc_username']
        new_password = request.form['confirm_new_password']

        if not db.admin.find_one({'username': local_username}):
            new_acc = {'username': local_username,
                    'password': model.encrypt_pswd(new_password)}

            db.admin.insert_one(new_acc)
            flash("Account added succesfully!", "success")

        else:
            flash("Account username already in use!", "danger")

    return render_template("admin.html", username=username, categories=model.categories)
   

@app.route("/order",methods=['GET','POST'])
def order():
    if "cart" not in session:
        flash("There's nothing in your cart!","danger")
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

    return redirect(url_for("menu",added=True))

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


@app.route("/search_receipt",methods=["POST"])
def search_receipt():
    receipt_number = request.form['look_up_number']
    return redirect(url_for('menu',receipt=receipt_number,search=True))