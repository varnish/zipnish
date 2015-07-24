from flask import Blueprint

api = Blueprint('api', __name__)

#
# end-points to create

# query
from . import query

#
# traces
# services
# spans
# annotations
# dependencies

# pin
from . import pin
