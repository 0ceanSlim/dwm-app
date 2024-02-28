from flask import g
from flask import current_app as app

import sqlite3, csv, os

DATABASE = "static/data/database.db"

breeding_pair_data = os.path.join('static', 'data', 'breeding_pair_data.csv')

def connect_db():
    return sqlite3.connect(DATABASE)

def before_request():
    g.db = connect_db()

def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()

def get_js_files():
    js_folder = os.path.join(app.static_folder, "js")
    js_files = [f for f in os.listdir(js_folder) if f.endswith(".js")]
    return js_files

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data