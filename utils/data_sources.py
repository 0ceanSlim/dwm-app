from flask import g
import os, sqlite3

DATABASE = "static/data/database.db"

def connect_db():
    return sqlite3.connect(DATABASE)

def before_request():
    g.db = connect_db()

def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()
        

breeding_pair_data = os.path.join('static', 'data', 'breeding_pair_data.csv')