from flask import Blueprint

application = Blueprint('application', __name__)

from . import views
