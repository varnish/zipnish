# web framework
from flask import Flask

# extensions
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
from config import config

# initialization
db = SQLAlchemy()

# called from the main app to create an application instance
def create_app(config_name):
    app = Flask(__name__)

    # configure application
    app.config.from_object(config[config_name])

    # initialize extensions
    db.init_app(app)

    # connect blueprints

    # /traces
    from .traces import traces as traces_blueprint
    app.register_blueprint(traces_blueprint, url_prefix='/traces')

    # /aggregate
    from .aggregate import aggregate as aggregate_blueprint
    app.register_blueprint(aggregate_blueprint, url_prefix='/aggregate')

    # /api
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
