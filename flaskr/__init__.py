import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

"""
I've used the Flask framework and its official documentation as reference
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/#application-setup
"""

# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/#application-setup
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exits, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  # Import and register close_db() and init_db_command()
  from . import db
  db.init_app(app)

  # Import and register the auth blueprint
  from . import auth
  app.register_blueprint(auth.bp)

  # Import and register the chat blueprint
  from . import chat
  app.register_blueprint(chat.bp)
  
  return app