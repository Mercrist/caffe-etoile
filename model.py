from Classes import Statics as local_data
from flask import current_app as app
from flask_pymongo import PyMongo
from dataclasses import asdict
import bcrypt

categories = ["Coffee", "Specialty Drinks", "Sandwiches", "Desserts"]
collections = ["menu", "receipt", "admin"]

def start_db()->"Database":
    """Starts a connection to the
       website's MongoDB database.

    Returns:
        Database: A MongoDB database object.
    """
    mongo = PyMongo(app)
    db = mongo.db
    return db

def encrypt_pswd(password:str)->bytes:
    """Encrypts a password with bcrypt
       and returns bcrypt's representation
       of the hash.

    Args:
        password (str): The password to hash, as a string.

    Returns:
        bytes: The hashed password in bytes, encoded by bcrypt.
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def reset_menu_collection()->None:
    """Resets the menu collection by
       clearing all its documents out
       and re-uploading the locally stored
       menu items. These initial items
       are later loaded onto the website.
    """
    #starts the db
    db = start_db()
    #access the menu collection
    db_menu = db.menu
    db_menu.delete_many({})

    #inserts the menu field into the mongodb database
    for item_obj in local_data.menu.values():
        db_menu.insert_one(asdict(item_obj))


def reset_receipts_collection()->None:
    """Resets the receipt collection by
       clearing all its documents out.
    """
    db = start_db()
    db.receipt.delete_many({})