from flask import Flask, render_template, g, abort, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "static/data/monsters.db"


def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


@app.route("/")
def show_index():
    return render_template("index.html")


@app.route("/get_families")
def get_families():
    cursor = g.db.cursor()
    cursor.execute("SELECT DISTINCT name FROM families")
    families = [row[0] for row in cursor.fetchall()]
    return jsonify(families)


@app.route("/get_monsters")
def get_monsters():
    selected_family = request.args.get("family")
    cursor = g.db.cursor()

    if selected_family:
        cursor.execute(
            """
            SELECT name FROM monsters
            WHERE family_id = (SELECT id FROM families WHERE name = ?)
        """,
            (selected_family,),
        )
    else:
        cursor.execute("SELECT DISTINCT name FROM monsters")

    monsters = [row[0] for row in cursor.fetchall()]
    return jsonify(monsters)


@app.route("/monster/<monster_name>")
def monster_info(monster_name):
    cursor = g.db.cursor()

    # Retrieve monster information from the database based on name
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

    monster_info = cursor.fetchone()

    if monster_info is None:
        abort(404)

    # Retrieve skills for the monster
    cursor.execute("SELECT skill FROM skills WHERE monster_id = ?", (monster_info[0],))
    skills = [row[0] for row in cursor.fetchall()]

    # Retrieve spawn locations for the monster
    cursor.execute(
        "SELECT map, description FROM spawn_locations WHERE monster_id = ?",
        (monster_info[0],),
    )
    spawn_locations = [
        {"map": row[0], "description": row[1]} for row in cursor.fetchall()
    ]

    return render_template(
        "monsters.html",
        monster={
            "id": monster_info[0],
            "name": monster_info[1],
            "family": monster_info[2],
            "in_story": "Yes" if monster_info[3] else "No",
            "agl": monster_info[4],
            "int": monster_info[5],
            "maxlvl": monster_info[6],
            "atk": monster_info[7],
            "mp": monster_info[8],
            "exp": monster_info[9],
            "hp": monster_info[10],
            "def": monster_info[11],
            "skills": skills,
            "spawn_locations": spawn_locations,
        },
    )

@app.route("/monster_info_json/<monster_name>")
def monster_info_json(monster_name):
    cursor = g.db.cursor()

    # Retrieve monster information from the database based on name
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

    monster_info = cursor.fetchone()

    if monster_info is None:
        abort(404)

    # Retrieve skills for the monster
    cursor.execute("SELECT skill FROM skills WHERE monster_id = ?", (monster_info[0],))
    skills = [row[0] for row in cursor.fetchall()]

    # Retrieve spawn locations for the monster
    cursor.execute(
        "SELECT map, description FROM spawn_locations WHERE monster_id = ?",
        (monster_info[0],),
    )
    spawn_locations = [
        {"map": row[0], "description": row[1]} for row in cursor.fetchall()
    ]

    return jsonify(
        monster={
            "id": monster_info[0],
            "name": monster_info[1],
            "family": monster_info[2],
            "in_story": "Yes" if monster_info[3] else "No",
            "agl": monster_info[4],
            "int": monster_info[5],
            "maxlvl": monster_info[6],
            "atk": monster_info[7],
            "mp": monster_info[8],
            "exp": monster_info[9],
            "hp": monster_info[10],
            "def": monster_info[11],
            "skills": skills,
            "spawn_locations": spawn_locations,
        }
    )


# Update the breeding route
@app.route("/breeding")
def breeding():
    # Get all monsters for dropdown
    cursor = g.db.cursor()
    cursor.execute("SELECT DISTINCT name FROM monsters")
    monsters = [row[0] for row in cursor.fetchall()]

    # Pass the monsters to the breeding template
    return render_template("breeding.html", monsters=monsters)


# Add this route for fetching breeding combinations
@app.route("/get_breeding_combinations")
def get_breeding_combinations():
    selected_monster = request.args.get("monster")
    if not selected_monster:
        return jsonify({"error": "Invalid input"})

    # Fetch breed ID based on the selected monster as a target
    breed_id = get_breed_id(selected_monster)

    if breed_id is None:
        return jsonify({"error": f"No breed information found for {selected_monster}"})

    base_combinations, mate_combinations = get_breeding_info(breed_id)

    return render_template(
        "breeding.html",
        selected_monster={
            "name": selected_monster,
            "base_combinations": base_combinations,
            "mate_combinations": mate_combinations,
        },
    )


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


def get_breeding_info(breed_id):
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

    base_combinations = [
        value
        for (requirement_type, value) in breeding_info
        if requirement_type == "base"
    ]
    mate_combinations = [
        value
        for (requirement_type, value) in breeding_info
        if requirement_type == "mate"
    ]

    return base_combinations, mate_combinations

@app.route("/footer")
def show_footer():
    return render_template("footer.html")

if __name__ == "__main__":
    app.run(debug=True)
