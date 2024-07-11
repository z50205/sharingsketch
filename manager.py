from flask import Flask
from flask.cli import FlaskGroup
from PSS import create_app,socketio
# from twittor.models.user import User


app = create_app()

# socketio.run(app)
# migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_shell_context():
#     # return dict(app=app, db=db, User=User)
#     return dict(app=app)

cli=FlaskGroup(app)

if __name__ == "__main__":
    cli()
    # app.run(debug= True)