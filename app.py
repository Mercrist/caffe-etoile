from flask import Flask, flash, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
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
    return render_template("menu.html", database=db, categories=model.categories)

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
                return redirect(url_for('admin'), code=307)

    return render_template("login.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
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
        if not db.menu.find_one({'name': item_name}):
            flash(f"{item_name} is not in the menu.", "danger")

        else:
            db.menu.delete_one({'name': item_name})
            flash(f"{item_name} was removed from the menu!", "success")

    elif 'remove_receipt_button' in request.form and request.form['remove_receipt_button'] == "clicked":
        receipt_number = request.form['remove_receipt_number']

        if not db.receipt.find_one({'receipt_num': receipt_number}):
            flash(f"Receipt #{receipt_number} does not exist.", "danger")

        else:
            db.receipt.delete_one({'receipt_num': receipt_number})
            flash(f"Receipt #{receipt_number} was removed from our logs!", "success")

    elif 'reset_menu_button' in request.form and request.form['reset_menu_button'] == "clicked":
        model.reset_menu_collection()

    elif 'reset_reservation_button' in request.form and request.form['reset_reservation_button'] == "clicked":
        model.reset_receipts_collection()

    return render_template("admin.html", categories=model.categories)
