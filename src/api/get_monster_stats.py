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
        query = """
            SELECT
                monsters.name,
                monsters.agl AS agility,
                monsters.int AS intelligence,
                monsters.maxlvl AS max_level,
                monsters.exp AS experience,
                monsters.hp AS health_points,
                monsters.atk AS attack,
                monsters.def AS defense,
                families.name AS family,
                spawn_locations.map || ' - ' || spawn_locations.description AS location,
                GROUP_CONCAT(skills.skill) AS skills
            FROM monsters
            LEFT JOIN families ON monsters.family_id = families.id
            LEFT JOIN spawn_locations ON monsters.id = spawn_locations.monster_id
            LEFT JOIN skills ON monsters.id = skills.monster_id
            WHERE LOWER(monsters.name) = LOWER(?)
            GROUP BY monsters.id
        """

        cursor.execute(query, (selected_monster.lower(),))

        # Fetch the result and convert it to a dictionary
        monster_stats = cursor.fetchone()
        print("Result:", monster_stats)

        if monster_stats:
            # Map stat names to descriptive labels
            stat_labels = {
                "max_level": "Max Level",
                "experience": "Experience",
                "health_points": "Health Points",
                "attack": "Attack",
                "defense": "Defense",
                "agility": "Agility",
                "intelligence": "Intelligence",
                "family": "Family",
                "location": "Location",
                "skills": "Skills"
            }

            # Create a new dictionary with descriptive stat names
            formatted_stats = {
                "name": monster_stats[0],
                **{stat_labels[key]: monster_stats[i + 1] for i, key in enumerate(["agility", "intelligence", "max_level", "experience", "health_points", "attack", "defense", "family", "location", "skills"])}
            }

            return jsonify(formatted_stats)
        else:
            return jsonify({"error": "Monster not found"}), 404
    else:
        return jsonify({"error": "Monster name not provided"}), 400
