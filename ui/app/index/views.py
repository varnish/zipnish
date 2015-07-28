from flask import request, redirect, render_template
from . import index

@index.route('/', methods=['GET'])
def index():
    return render_template('index.html')