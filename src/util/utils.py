import sqlite3, csv

DATABASE = "src/data/database.db"

def connect_db():
    return sqlite3.connect(DATABASE)

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data