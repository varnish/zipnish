from flask import render_template, request, redirect
from . import api

@api.route('/services')
def services():
    return '/services'
