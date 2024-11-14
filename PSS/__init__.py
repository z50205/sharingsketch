from flask import Flask
from PSS.extensions import db,migrate,login_manager,mail
from PSS.config import Config
from PSS.route import index,room,register,room_choose,gallery_export,membership,logout
from PSS.events import socketio
from gevent import monkey

monkey.patch_all()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    socketio.init_app(app, cors_allowed_origins=['http://127.0.0.1:5000','http://localhost','http://localhost:8002','https://bizara.link'], message_queue='redis://redis:6379',max_http_buffer_size=20*1024*1024,logger=True,always_connect =True)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    app.config["DEBUG"]=True
    print(f'SQLALCHEMY_DATABASE_URI={app.config["SQLALCHEMY_DATABASE_URI"]}')
    app.add_url_rule('/','index',index,methods=['GET','POST'])
    app.add_url_rule('/register','register',register,methods=['GET','POST'])
    app.add_url_rule('/room','room',room,methods=['GET','POST'])
    app.add_url_rule('/rooms','room_choose',room_choose,methods=['GET','POST'])
    app.add_url_rule('/export','gallery_export',gallery_export,methods=['GET','POST'])
    app.add_url_rule('/logout','logout',logout,methods=['GET','POST'])
    app.add_url_rule('/membership','membership',membership,methods=['GET'])
    @app.after_request
    def add_header(r):
        r.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        r.headers["Surrogate-Control"] = "no-store"
        return r
    return app


