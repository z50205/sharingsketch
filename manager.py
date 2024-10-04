from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from flask_cors import CORS
from PSS import create_app,db
from PSS.models.user import User



app = create_app()

# CORS(app,resources={r"/*": {"origins": "https://beamviewer.bizara.link"}})
CORS(app,resources={r"/*": {"origins": ["http://13.112.29.121/","http://13.112.29.121:8000","http://localhost:3001","http://127.0.0.1:5000",'http://localhost:3000','http://localhost:5000']}}, supports_credentials=True)
# socketio.run(app)
# migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(app=app, db=db, User=User)

cli=FlaskGroup(app)

if __name__ == "__main__":
    cli()
    # app.run(debug= True,host='localhost',port=8002)
    # app.run(debug= True,port=5000)