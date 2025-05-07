from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    login = StringField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Repeat password', validators=[DataRequired()])
    surname = PasswordField('Surname', validators=[DataRequired()])
    name = PasswordField('Name', validators=[DataRequired()])
    age = PasswordField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = PasswordField('Speciality', validators=[DataRequired()])
    address = PasswordField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')