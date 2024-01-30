from flask import Flask, render_template, g, abort, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'static/data/monsters.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/")
def show_index():
    return render_template("index.html")

@app.route('/get_families')
def get_families():
    cursor = g.db.cursor()
    cursor.execute('SELECT DISTINCT name FROM families')
    families = [row[0] for row in cursor.fetchall()]
    return jsonify(families)

@app.route('/get_monsters')
def get_monsters():
    selected_family = request.args.get('family')
    cursor = g.db.cursor()

    if selected_family:
        cursor.execute('''
            SELECT name FROM monsters
            WHERE family_id = (SELECT id FROM families WHERE name = ?)
        ''', (selected_family,))
    else:
        cursor.execute('SELECT DISTINCT name FROM monsters')

    monsters = [row[0] for row in cursor.fetchall()]
    return jsonify(monsters)

@app.route('/monster/<monster_name>')
def monster_info(monster_name):
    cursor = g.db.cursor()

    # Retrieve monster information from the database based on name
    cursor.execute('''
        SELECT
            monsters.id, monsters.name, families.name AS family, monsters.in_story,
            monsters.agl, monsters.int, monsters.maxlvl, monsters.atk, monsters.mp,
            monsters.exp, monsters.hp, monsters.def
        FROM
            monsters
        JOIN families ON monsters.family_id = families.id
        WHERE
            monsters.name = ?
    ''', (monster_name,))

    monster_info = cursor.fetchone()

    if monster_info is None:
        abort(404)

    # Retrieve skills for the monster
    cursor.execute('SELECT skill FROM skills WHERE monster_id = ?', (monster_info[0],))
    skills = [row[0] for row in cursor.fetchall()]

    # Retrieve spawn locations for the monster
    cursor.execute('SELECT map, description FROM spawn_locations WHERE monster_id = ?', (monster_info[0],))
    spawn_locations = [{'map': row[0], 'description': row[1]} for row in cursor.fetchall()]

    return render_template('monsters.html', monster={
        'id': monster_info[0],
        'name': monster_info[1],
        'family': monster_info[2],
        'in_story': 'Yes' if monster_info[3] else 'No',
        'agl': monster_info[4],
        'int': monster_info[5],
        'maxlvl': monster_info[6],
        'atk': monster_info[7],
        'mp': monster_info[8],
        'exp': monster_info[9],
        'hp': monster_info[10],
        'def': monster_info[11],
        'skills': skills,
        'spawn_locations': spawn_locations
    })
    
if __name__ == '__main__':
    app.run(debug=True)
