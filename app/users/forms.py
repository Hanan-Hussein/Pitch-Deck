from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from app.models import User
    
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



class ForgotPassword(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')

class VerifyOtp(FlaskForm):
    otp=StringField('Otp', validators=[DataRequired()])
    submit = SubmitField('Verify')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

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
