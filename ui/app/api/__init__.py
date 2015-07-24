from flask import Blueprint

api = Blueprint('api', __name__)

#
# end-points to create

# query
from . import query

# services
from . import services

#
# traces
# services
# spans
# annotations
# dependencies

# pin
from . import pin
