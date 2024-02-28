from flask import Blueprint, g, jsonify

get_families_bp = Blueprint('families', __name__)

# List All Families
@get_families_bp.route("/api/families")
def get_families():
    cursor = g.db.cursor()
    cursor.execute("SELECT DISTINCT name FROM families")
    families = [row[0] for row in cursor.fetchall()]
    return jsonify(families)