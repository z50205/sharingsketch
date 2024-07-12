from flask import Flask


from PSS.events import socketio
from PSS.route import index
def create_app():
    app=Flask(__name__)
    app.config["DEBUG"]=True
    app.config["SECRET_KEY"]="secret"
    app.add_url_rule('/','index',index,methods=['GET','POST'])
    socketio.init_app(app, cors_allowed_origins='https://beamviewer.bizara.link')
    # socketio.init_app(app)
    return app