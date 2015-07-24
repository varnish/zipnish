from flask import Blueprint

api = Blueprint('api', __name__)

#
# Blueprints to create
#
# traces
# services
# spans
# annotations
# dependencies

# pin
from . import pin
