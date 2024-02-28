from flask import current_app as app

import csv, os

def get_js_files():
    js_folder = os.path.join(app.static_folder, "js")
    js_files = [f for f in os.listdir(js_folder) if f.endswith(".js")]
    return js_files

def read_skills_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data