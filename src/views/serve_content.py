from flask import send_from_directory, Blueprint

serve_favicon_bp = Blueprint('favicon', __name__)
serve_monster_sprite_bp = Blueprint('monster_sprite', __name__)

#Serve Monster Sprites
@serve_favicon_bp.route('/img/monster/<selected_monster>.png')
def serve_monster_sprite(selected_monster):
    return send_from_directory('static/img/monster/', f'{selected_monster}.png')

#Serve Favicon
@serve_monster_sprite_bp.route('/img/favicon.ico')
def serve_favicon():
    return send_from_directory( '','static/img/favicon.ico')