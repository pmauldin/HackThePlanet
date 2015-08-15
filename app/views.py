from flask import render_template, request, send_from_directory
from app import app

@app.route('/')
def index():
    return render_template('index.html')

