from flask import Flask, render_template

from src.util.utils import *

from src.api.get_monsters import *
from src.api.get_families import *
from src.api.get_monster_stats import *
from src.api.get_breeding_pairs import *
from src.api.get_breeding_usage import *
from src.api.get_skills_data import *

from src.util.serve_media import *

#from src.views.skills import *

app = Flask(__name__)

# Utils
app.before_request(before_request)
app.teardown_request(teardown_request)

# Register API Blueprints
app.register_blueprint(get_families_bp)
app.register_blueprint(get_monsters_bp)
app.register_blueprint(get_monster_stats_bp)
app.register_blueprint(get_breeding_pairs_bp)
app.register_blueprint(get_breeding_usage_bp)
app.register_blueprint(get_skills_data_bp)

# Register Serve Content Blueprints
app.register_blueprint(serve_media)

# Register Other Views Blurprints (HTML Render Templates)
#app.register_blueprint(skills_bp)

@app.route("/")
def show_app():
    js_files = get_js_files()
    return render_template("app.html", js_files=js_files)

@app.route('/skills')
def skills():
    csv_data = read_csv('static/data/skills_data.csv')
    return render_template('skills.html', csv_data=csv_data)

if __name__ == "__main__":
    app.run(debug=True)
