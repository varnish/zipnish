from flask import render_template, request, redirect
from . import api

@api.route('/pin/<pin_id>/<state>', methods=['GET'])
def pin(pin_id, state):
    return '/api/pin/%s/%s' % (pin_id, state)
