from flask import Blueprint

public = Blueprint('public', __name__)

from . import views
