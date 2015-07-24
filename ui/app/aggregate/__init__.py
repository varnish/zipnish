from flask import Blueprint

aggregate = Blueprint('aggregate', __name__)

from . import views
