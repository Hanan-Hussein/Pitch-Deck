from app.models import User, Pitch, Otp
from flask import render_template, url_for, Blueprint

main= Blueprint('main',__name__)

@main.route('/')
def home():
    # All pitches here
    pitches = Pitch.query.all()

    # comments_list = comments_cutter(pitches.comments)
    return render_template('index.html', pitches=pitches)

