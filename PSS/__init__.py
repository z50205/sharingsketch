from flask import Flask
from PSS.extensions import db,migrate,login_manager,mail
from PSS.config import Config
from PSS.route import index,room,register,intro
from PSS.events import socketio

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    # socketio.init_app(app)
    # socketio.init_app(app, cors_allowed_origins='https://beamviewer.bizara.link')
    socketio.init_app(app, cors_allowed_origins=['http://52.195.89.113','http://52.195.89.113:8002'])
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    app.config["DEBUG"]=True
    # app.config["SECRET_KEY"]="secret"
    app.add_url_rule('/','index',index,methods=['GET','POST'])
    app.add_url_rule('/register','register',register,methods=['GET','POST'])
    app.add_url_rule('/room','room',room,methods=['GET','POST'])
    return app