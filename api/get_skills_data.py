from flask import Blueprint, jsonify
import csv

get_skills_data_bp = Blueprint('skills_data',__name__)

# Load data from CSV file
def load_data():
    data = []
    with open('static/data/skills_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Endpoint to get all skills
@get_skills_data_bp.route('/api/skills', methods=['GET'])
def get_all_skills():
    skills = load_data()
    return jsonify(skills)
