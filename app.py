from flask import Flask, render_template, g, abort, request, jsonify, send_from_directory
import sqlite3, os

from src.python.breed import get_breed_id, get_breeding_pairs, get_used_in_breeds

app = Flask(__name__)

DATABASE = "src/database.db"


def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


def get_js_files():
    js_folder = os.path.join(app.static_folder, "js")
    js_files = [f for f in os.listdir(js_folder) if f.endswith(".js")]
    return js_files


@app.route("/")
def show_app():
    js_files = get_js_files()
    return render_template("app.html", js_files=js_files)

#Serve Monster Sprites
@app.route('/img/monster/<selected_monster>.png')
def serve_monster_sprite(selected_monster):
    return send_from_directory('static/img/monster/', f'{selected_monster}.png')

#Serve Favicon
@app.route('/img/favicon.ico')
def serve_favicon():
    return send_from_directory( '','static/img/favicon.ico')

#API Calls

# List All Families
@app.route("/api/families")
def json_families():
    cursor = g.db.cursor()
    cursor.execute("SELECT DISTINCT name FROM families")
    families = [row[0] for row in cursor.fetchall()]
    return jsonify(families)

# List All Monsters
@app.route("/api/monsters")
def json_monsters():
    selected_family = request.args.get("family")
    cursor = g.db.cursor()

    if selected_family:
        cursor.execute(
            """
            SELECT name
            FROM monsters
            WHERE family_id = (SELECT id FROM families WHERE name = ?)
            ORDER BY (agl + int + atk + mp + exp + hp + def) * maxlvl ASC
        """,
            (selected_family,),
        )
    else:
        cursor.execute(
            """
            SELECT name
            FROM monsters
            ORDER BY (agl + int + atk + mp + exp + hp + def) * maxlvl ASC
            """
        )

    monsters = [row[0] for row in cursor.fetchall()]
    return jsonify(monsters)


@app.route("/api/monsters/stats")
def json_monsters_stats():
    cursor = g.db.cursor()

    # Check if 'monster' argument is provided
    selected_monster = request.args.get("monster")

    if selected_monster:
        # Fetch specific stats for the monster
        cursor.execute("""
            SELECT
                name,
                agl AS agility,
                int AS intelligence,
                maxlvl AS max_level,
                exp AS experience,
                hp AS health_points,
                atk AS attack,
                def AS defense
            FROM monsters
            WHERE LOWER(name) = LOWER(?)
        """, (selected_monster.lower(),))

        # Fetch the result and convert it to a dictionary
        monster_stats = cursor.fetchone()

        if monster_stats:
            # Map stat names to descriptive labels
            stat_labels = {
                "max_level": "Max Level",
                "experience": "Experience",
                "health_points": "Health Points",
                "attack": "Attack",
                "defense": "Defense",
                "agility": "Agility",
                "intelligence": "Intelligence"            
                }

            # Create a new dictionary with descriptive stat names
            formatted_stats = {
                "name": monster_stats[0],
                **{stat_labels[key]: monster_stats[i + 1] for i, key in enumerate(["agility", "intelligence", "max_level", "experience", "health_points", "attack", "defense"])}
            }

            return jsonify(formatted_stats)
        else:
            return jsonify({"error": "Monster not found"}), 404
    else:
        return jsonify({"error": "Monster name not provided"}), 400
    
# Render HTML Templates

@app.route("/monster/<monster_name>")
def monster_stats(monster_name):
    cursor = g.db.cursor()

    # Retrieve monster stats from the database based on name
    cursor.execute(
        """
        SELECT
            monsters.id, monsters.name, families.name AS family, monsters.in_story,
            monsters.agl, monsters.int, monsters.maxlvl, monsters.atk, monsters.mp,
            monsters.exp, monsters.hp, monsters.def
        FROM
            monsters
        JOIN families ON monsters.family_id = families.id
        WHERE
            monsters.name = ?
    """,
        (monster_name,),
    )

    monster_stats = cursor.fetchone()

    if monster_stats is None:
        abort(404)

    # Retrieve skills for the monster
    cursor.execute("SELECT skill FROM skills WHERE monster_id = ?", (monster_stats[0],))
    skills = [row[0] for row in cursor.fetchall()]

    # Retrieve spawn locations for the monster
    cursor.execute(
        "SELECT map, description FROM spawn_locations WHERE monster_id = ?",
        (monster_stats[0],),
    )
    spawn_locations = [
        {"map": row[0], "description": row[1]} for row in cursor.fetchall()
    ]

    return render_template(
        "stats.html",
        monster={
            "id": monster_stats[0],
            "name": monster_stats[1],
            "family": monster_stats[2],
            "in_story": "Yes" if monster_stats[3] else "No",
            "agl": monster_stats[4],
            "int": monster_stats[5],
            "maxlvl": monster_stats[6],
            "atk": monster_stats[7],
            "mp": monster_stats[8],
            "exp": monster_stats[9],
            "hp": monster_stats[10],
            "def": monster_stats[11],
            "skills": skills,
            "spawn_locations": spawn_locations,
        },
    )


# Add this route for fetching breeding combinations
@app.route("/breed")
def get_breeding_combinations():
    selected_monster = request.args.get("monster")
    if not selected_monster:
        return jsonify({"error": "Invalid input"})

    # Fetch breed ID based on the selected monster as a target
    breed_id = get_breed_id(selected_monster)

    if breed_id is None:
        return jsonify({"error": f"No breed information found for {selected_monster}"})

    base_pair, mate_pair = get_breeding_pairs(breed_id)

    # Fetch breeds in which the selected monster is used
    used_in_breeds = get_used_in_breeds(selected_monster)

    return render_template(
        "breed.html",
        selected_monster={
            "name": selected_monster,
            "base_pair": base_pair,
            "mate_pair": mate_pair,
        },
        used_in_breeds=used_in_breeds,
    )

if __name__ == "__main__":
    app.run(debug=True)
