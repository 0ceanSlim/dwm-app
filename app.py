from flask import Flask, render_template

from api.get_monsters import *
from api.get_families import *
from api.get_monster_stats import *
from api.get_breeding_pairs import *
from api.get_breeding_usage import *
from api.get_skills_data import *

from utils.utils import *
from utils.serve_media import *
from utils.data_sources import *

app = Flask(__name__)

# Utils
app.before_request(before_request)
app.teardown_request(teardown_request)
app.register_blueprint(serve_media)

# Register API Blueprints
app.register_blueprint(get_families_bp)
app.register_blueprint(get_monsters_bp)
app.register_blueprint(get_monster_stats_bp)
app.register_blueprint(get_breeding_pairs_bp)
app.register_blueprint(get_breeding_usage_bp)
app.register_blueprint(get_skills_data_bp)


@app.route("/")
def show_app():
    js_files = get_js_files()
    return render_template("app.html", js_files=js_files)

@app.route('/skills')
def skills():
    csv_data = read_skills_csv('static/data/skills_data.csv')
    return render_template('skills.html', csv_data=csv_data)

if __name__ == "__main__":
    app.run(debug=True)
