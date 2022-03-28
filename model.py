from Classes import Statics as local_data
from flask import current_app as app
from flask_pymongo import PyMongo
from dataclasses import asdict

categories = ["Coffee", "Specialty Drinks", "Sandwiches", "Desserts"]

def reset_menu_collection()->None:
    """Resets the menu collection by 
       clearing all its documents out
       and re-uploading the locally stored 
       menu items which are then loaded
       on the website.
    """
    #starts the db
    mongo = PyMongo(app)
    db = mongo.db
    #access the menu collection
    db_menu = db.menu
    db_menu.delete_many({})

    #inserts the menu field into the mongodb database
    for item_obj in local_data.menu.values():
        db_menu.insert_one(asdict(item_obj)) 