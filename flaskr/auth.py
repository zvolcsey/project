import functools

from flask import (
  Blueprint, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

"""
I've used the Flask framework and its official documentation as reference
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#blueprints-and-views
"""

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  """Register user"""

  # Forget any user_id
  session.clear()

  # User submit the register form with POST method
  if request.method == 'POST':
    username = request.form["username"]
    password = request.form["password"]
    confirmation = request.form["confirmation"]
    db = get_db()

    # Ensure username was submitted
    if not username:
      return render_template("error.html", status=400, message="must provide username")

    # Ensure password was submitted
    if not password:
      return render_template("error.html", status=400, message="must provide password")

    # Ensure confirmation was submitted
    if not confirmation:
      return render_template("error.html", status=400, message="must provide confirmation")
    
    # Ensure password was matched with password confirmation
    if password != confirmation:
      return render_template("error.html", status=400, message="passwords don't match")
    
    try:
      # Begin a transaction
      db.execute("BEGIN;")

      # Query database fro username
      rows = db.execute(
        "SELECT username FROM users WHERE username = ?", (username,)
      ).fetchone()

      if rows is not None:
        return render_template("error.html", status=400, message="username already exists")

      # Hash the password
      hash = generate_password_hash(password)

      # Add user to the database
      user_id = db.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?) RETURNING id",
        (username, hash)
      ).fetchone()

      # Commit the transaction
      db.execute("COMMIT;")

      db.commit()

    except Exception as e:
      # If the transaction fails run "ROLLBACK", print an error and render the error.html
      db.execute("ROLLBACK;")
      print(e)
      return render_template("error.html", status=500, message="transaction was NOT successfull")
    
    # Log user in
    session["user_id"] = user_id["id"]

    # Redirect user to the index page
    return redirect(url_for("chat.index"))

  # Render the register page with GET method
  return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
  """Log user in"""

  # Forget any user_id
  session.clear()

  # User submit the login form with POST method
  if request.method == 'POST':
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()

    # Ensure username was submitted
    if not username:
      return render_template("error.html", status=403, message="must provide username")

    # Ensure password was submitted
    if not password:
      return render_template("error.html", status=403, message="must provide username")

    # Query database
    rows = db.execute(
      "SELECT * FROM users WHERE username = ?;", (username,)
    ).fetchone()

    # Ensure username exists
    if rows is None:
      return render_template("error.html", status=403, message="invalid username")

    # Ensure username exists and password is correct
    if not check_password_hash(
      rows["hash"], password
    ):
      return render_template("error.html", status=403, message="invalid password")
    
    # Remember which user has logged in
    session["user_id"] = rows["id"]

    # Redirect user to the index page
    return redirect(url_for("chat.index"))

  else:
    # Render the login page with GET method
    return render_template("auth/login.html")

# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#login
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    db = get_db()
    g.user = db.execute(
      'SELECT * FROM users WHERE id=?', (user_id,)
    ).fetchone()

# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#logout
@bp.route('/logout', methods=('GET', 'POST'))
def logout():
  session.clear()
  return redirect(url_for("auth.login"))


# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#require-authentication-in-other-views
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    
    return view(**kwargs)
  
  return wrapped_view