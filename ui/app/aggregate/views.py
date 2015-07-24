from flask import render_template, request, redirect
from . import aggregate

@aggregate.route('/', methods=['GET'])
def app():
    return '/aggregate'
