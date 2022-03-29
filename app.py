from flask import Flask, flash, url_for, redirect, request, render_template
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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        #add menu item button was clicked
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

        elif 'reset_menu_button' in request.form and request.form['reset_menu_button'] == "clicked":
            model.reset_menu_collection()

        return redirect(url_for('admin'))
        

    return render_template("admin.html", categories=model.categories)