from flask import Blueprint, render_template, g, request
import jsonify

breed_info_bp = Blueprint('view_breed_info', __name__)

@breed_info_bp.route("/breed")
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