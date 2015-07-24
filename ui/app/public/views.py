from flask import render_template, request, redirect
from . import public

@public.route('/', methods=['GET'])
def public():
    return '/public'
