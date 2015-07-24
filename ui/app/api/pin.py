from flask import render_template, request, redirect
from . import api

@api.route('/is_pinned/<pin_id>', methods=['GET'])
def is_pinned(pin_id):
    return '/api/is_pinned/%s' % pin_id

@api.route('/pin/<pin_id>/<state>', methods=['GET'])
def pin(pin_id, state):
    return '/api/pin/%s/%s' % (pin_id, state)
