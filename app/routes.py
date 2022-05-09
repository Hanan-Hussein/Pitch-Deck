from flask import render_template, url_for, flash, redirect, request
from . import app, db, bcrypt
from app.models import User,Pitch
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import Register, Login,PitchForm
db.create_all()


@app.route('/')
def home():
    pitches = Pitch.query.all()
    
    return render_template('index.html',pitches=pitches)