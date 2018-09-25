import os

from flask import Flask, Markup, render_template, jsonify, request
from bokeh.embed import server_document
from .plant_data import plant_data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'plant.sqlite'))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def index():
        script = server_document('http://localhost:5006/bok')
        return render_template('index.html', bokeh_script=Markup(script), options=plant_data)

    @app.route('/plants', methods=['POST'])
    def plants():
        plant_name = request.form['plant_name']
        return jsonify(plant_data[plant_name])

    from . import db
    db.init_app(app)

    return app