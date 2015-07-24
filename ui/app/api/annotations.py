from flask import render_template, request, redirect
from . import api

@api.route('/top_annotations')
def top_annotations():
    return '/top_annotations'
