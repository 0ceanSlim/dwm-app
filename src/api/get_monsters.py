from flask import Blueprint, g, jsonify, request

get_monsters_bp = Blueprint('monsters', __name__)

# List All Monsters
@get_monsters_bp.route("/api/monsters")
def get_monsters():
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