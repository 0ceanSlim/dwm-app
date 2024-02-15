from flask import Blueprint, g, jsonify, request

get_monster_stats_bp = Blueprint('monster_stats', __name__)

# List All Monsters
@get_monster_stats_bp.route("/api/monster/stats")
def get_monster_stats():
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