from flask import Blueprint

traces = Blueprint('traces', __name__)

from . import views
