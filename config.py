import os
SECRET_KEY = os.urandom(16).hex()
MONGO_DBNAME = 'mainframe'
MONGO_URI = f"mongodb+srv://mainframe:WlZZs0TzAwc9j2IN@cluster0.ftsgg.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority"