from flask import Flask, render_template

from src.util.utils import *

from src.api.get_monsters import *
from src.api.get_families import *
from src.api.get_monster_stats import *
from src.api.get_breeding_pairs import *

from src.views.serve_content import *
from src.views.breed_info import *
from src.views.skills import *

app = Flask(__name__)

# Utils
app.before_request(before_request)
app.teardown_request(teardown_request)

# Register API Blueprints
app.register_blueprint(get_families_bp)
app.register_blueprint(get_monsters_bp)
app.register_blueprint(get_monster_stats_bp)
app.register_blueprint(get_breeding_pairs_bp)

# Register Serve Content Blueprints
app.register_blueprint(serve_content)

# Register Other Views Blurprints (HTML Render Templates)
app.register_blueprint(breed_info_bp)
app.register_blueprint(skills_bp)

@app.route("/")
def show_app():
    js_files = get_js_files()
    return render_template("app.html", js_files=js_files)

if __name__ == "__main__":
    app.run(debug=True)
