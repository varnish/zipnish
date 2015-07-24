from flask import render_template, request, redirect
from . import api

@api.route('/dependencies', methods=['GET'])
def dependencies():
    return '/dependencies'

@api.route('/dependencies/<start_time>/<end_time>', methods=['GET'])
def dependenciesTimeBound(start_time=None, end_time=None):
    return '/dependencies/%s/%s' % (start_time, end_time)
