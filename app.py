from flask import Flask, render_template, g, abort, request, jsonify

from src.api.get_monsters import *
from src.api.get_families import *
from src.api.get_monster_stats import *

from src.util.utils import *

from src.views.serve_content import *

app = Flask(__name__)

# Utils
app.before_request(before_request)
app.teardown_request(teardown_request)

# Register Serve Content Blueprints
app.register_blueprint(serve_favicon_bp)
app.register_blueprint(serve_monster_sprite_bp)

# Register API Blueprints
app.register_blueprint(get_families_bp)
app.register_blueprint(get_monsters_bp)
app.register_blueprint(get_monster_stats_bp)

@app.route("/")
def show_app():
    js_files = get_js_files()
    return render_template("app.html", js_files=js_files)


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
    
def get_used_in_breeds(target_monster):
    cursor = g.db.cursor()

    # Fetch breed IDs where the selected monster is used as a base
    cursor.execute(
        """
        SELECT breed_id
        FROM breed_requirements
        WHERE requirement_type = 'base'
              AND requirement_value = ?
        """,
        (target_monster,),
    )

    base_breed_ids = [row[0] for row in cursor.fetchall()]

    # Fetch breed IDs where the selected monster is used as a mate
    cursor.execute(
        """
        SELECT breed_id
        FROM breed_requirements
        WHERE requirement_type = 'mate'
              AND requirement_value = ?
        """,
        (target_monster,),
    )

    mate_breed_ids = [row[0] for row in cursor.fetchall()]

    # Combine the results from both queries
    used_in_breed_ids = base_breed_ids + mate_breed_ids

    # Fetch the target monsters for the obtained breed IDs
    used_in_breeds = []
    for breed_id in used_in_breed_ids:
        cursor.execute(
            """
            SELECT target
            FROM breeds
            WHERE id = ?
            """,
            (breed_id,),
        )
        target_monster = cursor.fetchone()
        if target_monster:
            used_in_breeds.append(target_monster[0])

    return used_in_breeds

def get_breed_id(target_monster):
    cursor = g.db.cursor()

    # Fetch breed ID based on the selected monster as a target
    cursor.execute(
        """
        SELECT breeds.id
        FROM breeds
        WHERE breeds.target = ?
        """,
        (target_monster,),
    )

    breed_id = cursor.fetchone()

    if breed_id:
        return breed_id[0]
    else:
        return None


def get_breeding_pairs(breed_id):
    cursor = g.db.cursor()

    # Fetch base and mate breeding combinations based on the breed ID
    cursor.execute(
        """
        SELECT requirement_type, requirement_value
        FROM breed_requirements
        WHERE breed_id = ?
        """,
        (breed_id,),
    )

    breeding_info = cursor.fetchall()

    base_pair = [
        value
        for (requirement_type, value) in breeding_info
        if requirement_type == "base"
    ]
    mate_pair = [
        value
        for (requirement_type, value) in breeding_info
        if requirement_type == "mate"
    ]

    return base_pair, mate_pair    

@app.route('/skills')
def skills():
    csv_data = read_csv('src/skills_data.csv')
    return render_template('skills.html', csv_data=csv_data)

if __name__ == "__main__":
    app.run(debug=True)
