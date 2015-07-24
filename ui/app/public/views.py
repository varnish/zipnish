from flask import render_template, request, redirect
from . import public

@public.route('/')
def app():
    return '/public'
