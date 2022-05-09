from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager

# The login in the init method


@login_manager.user_loader
def login_manager(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    The table for the User in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile = db.Column(db.String, nullable=False, default='anon.png')
    pitches = db.relationship('Pitch', backref='author', lazy=True)

    def __repr__(self):
        return f"id: {self.id} , username: {self.username} "


class Pitch(db.Model):
    """
    The talbe for the Pitches

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"id: {self.id} , title: {self.title}"
