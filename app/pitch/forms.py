from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,RadioField
from flask_wtf import FlaskForm

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
