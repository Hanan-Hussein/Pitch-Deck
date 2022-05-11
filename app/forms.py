from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed


class Register(FlaskForm):
    """_summary_

    Args:
        Form (_type_): _description_
    """
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])

    submit = SubmitField('Signup')

    def validate_username(self, username):
        """
        """
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(
                "That username is already taken! Please choose another")

    def validate_email(self, email):
        """

        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is already taken! Please choose another")


class Login(FlaskForm):
    """

    Args:
        Form (_type_): _description_
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PitchForm(FlaskForm):
    """
    Args:
        FlaskForm (_type_): _description_
    """
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired(),Length(min=2, max=300)])
    submit = SubmitField('Create Pitch')
    category=RadioField('Category', choices = [('Tech','Tech'),('Transport','Transport'),('Agriculture','Agriculture'),('Health','Health')])
    
class CommentsForm(FlaskForm):
    content=TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')

class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
     
    picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    Submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one")

    def validate_email(self, email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one")

