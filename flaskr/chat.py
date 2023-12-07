from flask import (
  Blueprint, render_template, session,
)

from flaskr.db import get_db
from flaskr.auth import login_required

"""
I've used the Flask framework and its official documentation as reference
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#blueprints-and-views
"""

bp = Blueprint('chat', __name__, url_prefix='/')

@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
  """Show the dashboard page"""

  # Get the logged user's id
  user_id = session.get("user_id")

  # Connect to the db
  db = get_db()

  # Query for user
  user = db.execute(
    "SELECT username FROM users WHERE id=?", (user_id,)
  ).fetchone()

  # Render the index.html template
  return render_template("chat/index.html", username=user["username"], found_users=None)