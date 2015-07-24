from flask import render_template, request, redirect
from . import application

@application.route('/', methods=['GET'])
def app():
    return '/app'
