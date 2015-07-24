from flask import render_template, request, redirect
from . import application

@application.route('/')
def app():
    return '/app'
