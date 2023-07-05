from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators= [DataRequired()])
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class MarvelForm(FlaskForm):
    name = StringField('Name')
    description = StringField('Description')
    comics_appeared_in = IntegerField('Comics appeared in')
    super_power = StringField('Super Power')
    date_created = DateField('Date Created')
    random_jokes = StringField('R')
    submit_button = SubmitField()





