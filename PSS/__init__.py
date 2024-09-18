from flask import Flask
from PSS.extensions import db,migrate,login_manager,mail
from PSS.config import Config
from PSS.route import index,room,register,intro,gallery_import,gallery_export,membership
from PSS.events import socketio

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    # socketio.init_app(app)
    # socketio.init_app(app, cors_allowed_origins='https://beamviewer.bizara.link')
    socketio.init_app(app, cors_allowed_origins=['http://13.112.29.121','http://13.112.29.121:8002','http://localhost:3001'])
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    app.config["DEBUG"]=True
    # app.config["SECRET_KEY"]="secret"
    print(f'SQLALCHEMY_DATABASE_URI={app.config["SQLALCHEMY_DATABASE_URI"]}')
    app.add_url_rule('/','index',index,methods=['GET','POST'])
    app.add_url_rule('/register','register',register,methods=['GET','POST'])
    app.add_url_rule('/room','room',room,methods=['GET','POST'])
    app.add_url_rule('/api/galleryImport','gallery_import',gallery_import,methods=['GET','POST'])
    app.add_url_rule('/api/galleryExport','gallery_export',gallery_export,methods=['GET','POST'])
    app.add_url_rule('/api/membership','membership',membership,methods=['GET'])
    return app


