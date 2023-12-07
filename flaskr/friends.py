from flask import (
  Blueprint, render_template, session, request, redirect
)

from flaskr.db import get_db
from flaskr.auth import login_required

"""
I've used the Flask framework and its official documentation as reference
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#blueprints-and-views
"""

bp = Blueprint('friends', __name__, url_prefix='/')

@bp.route("/search", methods=(["POST"]))
@login_required
def search():
  user_id = session.get("user_id")
  username = request.form["username"]
  db = get_db()

  # Ensure username was submitted
  if not username:
    return render_template("error.html", status=400, message="must provide username")
  
  try:
    user = db.execute(
      "SELECT username FROM users WHERE id = ?;", (user_id,)
    ).fetchone()

    found_users = db.execute(
      "SELECT username FROM users WHERE username LIKE ?;", (username + "%",)
    ).fetchall()
    
  except Exception as e:
    print(e)
    return render_template("error.html", status=500, message="something went wrong")

  return render_template("chat/index.html", username=user["username"], found_users=found_users)