from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('Team Leader id', validators=[DataRequired()])
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('is job finished?',)
    submit = SubmitField('Submit')


class RegForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
