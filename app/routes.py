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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has been Created! You are now able to login  in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
