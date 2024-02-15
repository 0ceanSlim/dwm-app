from flask import Blueprint, render_template

from ..util.utils import *

skills_bp = Blueprint('skills', __name__)
serve_monster_sprite_bp = Blueprint('monster_sprite', __name__)

#Serve Monster Sprites
@skills_bp.route('/skills')
def skills():
    csv_data = read_csv('src/skills_data.csv')
    return render_template('skills.html', csv_data=csv_data)