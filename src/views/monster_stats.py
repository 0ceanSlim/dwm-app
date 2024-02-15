from flask import Blueprint, render_template, abort, g

monster_stats_bp = Blueprint('view_monster_stats', __name__)

@monster_stats_bp.route("/monster/<monster_name>")
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
