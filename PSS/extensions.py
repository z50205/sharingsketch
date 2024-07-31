from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators,PasswordField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

socketio=SocketIO()
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()
mail=Mail()
login_manager.login_view='index'


class Loginform(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    roomname=StringField("Roomname",validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit =SubmitField('SignIn')

class Registerform(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired()])
    submit =SubmitField('Register')