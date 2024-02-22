from flask import Flask, jsonify, request, Blueprint

get_breeding_pairs_bp = Blueprint('breeding_pairs',__name__)

import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the CSV file in the data directory
csv_file_path = os.path.join(script_dir, '..', 'data', 'updated_breeding_pairs.csv')

# Read the CSV file and store breeding information
breeding_info = []
with open(csv_file_path, 'r') as file:
    lines = file.readlines()
    header = lines[0].strip().split(',')
    for line in lines[1:]:
        data = line.strip().split(',')
        breeding_info.append(dict(zip(header, data)))

def get_breeding_pairs(monster):
    pairs = []
    for entry in breeding_info:
        if entry['base'].lower() == monster.lower() or entry['mate'].lower() == monster.lower():
            pairs.append({'base': entry['base'], 'mate': entry['mate'], 'offspring': entry['offspring']})
    return pairs

#def get_usage_list(monster):
#    used_in = []
#    for entry in breeding_info:
#        if entry['offspring'].lower() == monster.lower():
#            used_in.append({'base': entry['base'], 'mate': entry['mate']})
#    return used_in

@get_breeding_pairs_bp.route('/breeding-pairs/<monster>', methods=['GET'])
def breeding_pairs(monster):
    pairs = get_breeding_pairs(monster)
    return jsonify({'breeding_pairs': pairs})

#@app.route('/usage-list/<monster>', methods=['GET'])
#def usage_list(monster):
#    used_in = get_usage_list(monster)
#    return jsonify({'used_in': used_in})
#

