from flask import render_template,redirect,url_for,abort,current_app,flash

def index():
    
    return render_template('index.html')