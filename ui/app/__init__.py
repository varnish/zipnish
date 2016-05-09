from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(db_dialect):

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_dialect

    db.init_app(app)

    # /app
    from .application import application as application_blueprint
    app.register_blueprint(application_blueprint, url_prefix='/app')

    # /public
    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint, url_prefix='/public')

    # /
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint, url_prefix='/')

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
