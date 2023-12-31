from flask import (
  Blueprint, render_template, redirect, url_for, session, request
)

from flaskr.db import get_db
from flaskr.auth import login_required
from flaskr.query_texts import *

import uuid

"""
I've used the Flask framework and its official documentation as reference
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/#blueprints-and-views
"""

bp = Blueprint('chat', __name__, url_prefix='/')

@bp.route("/", methods=["GET"])
@login_required
def index():
  """Show the dashboard page"""

  # Get the logged user's id
  user_id = session.get("user_id")

  # Connect to the db
  db = get_db()

  # Query for user
  user = db.execute(getUserByIdText(), (user_id,)).fetchone()

  # Render the index.html template
  return render_template("chat/index.html", username=user["username"], found_users=None)

@bp.route("/search", methods=(["GET"]))
@login_required
def search():
  """Search users"""

  # Get session and request data
  user_id = session.get("user_id")
  username = request.args.get("q")

  # Connect the db
  db = get_db()

  # Ensure username as query was submitted
  if not username:
    return render_template("error.html", status=400, message="must provide query")
  
  # Select logged user's data
  user = db.execute(
    getUserByIdText(), (user_id,)
  ).fetchone()

  if user is None:
    return render_template("error.html", status=400, message="must provide query")

  # Search users
  found_users = db.execute(
    searchUserText(), (username + "%",)
  ).fetchall()
  
  if found_users is None:
    return render_template("error.html", status=400, message="must provide query")

  # Render index.html with users list
  return render_template("chat/index.html", username=user["username"], found_users=found_users)

@bp.route("/send-message", methods=["POST"])
@login_required
def send_message():
  """Show chat UI"""

  user_id = session.get("user_id")
  username = request.form["username"]

  # Connect to the db
  db = get_db()

  # Query for sender
  logged_user = db.execute(getUserByIdText(), (user_id,)).fetchone()

  if logged_user is None:
    return render_template("error.html", status=400, message="logged user's data not found")

  # Query for recipient
  user_result = db.execute(getUserByUsernameText(), (username,)).fetchone()
  
  if user_result is None:
    return render_template("error.html", status=400, message="recipient user's data not found")

  # Ensure logged user's id and recipient's id was not the same
  if logged_user["id"] == user_result["id"]:
    return render_template("error.html", status=400, message="you can't have a chat with yourself")

  resource_id = None

  # Lookup the room's resource_id
  resource_id_result = db.execute(getChatByParticipantsText(), (
    logged_user["id"], 
    user_result["id"],
    user_result["id"],
    logged_user["id"]
  )).fetchone()

  # If the chat room does NOT exist, then create a room
  if resource_id_result is None:

    # Generate unique room_id
    resource_id = str(uuid.uuid4())

    smaller_id = None
    higher_id = None

    if user_id < int(user_result["id"]):
      smaller_id = user_id
      higher_id = int(user_result["id"])
    else:
      smaller_id = int(user_result["id"])
      higher_id = user_id

    # Create a private room
    db.execute(insertChatText(), (
      resource_id, 
      smaller_id,
      higher_id
    )).fetchone()

    db.commit()
  else:
    resource_id = resource_id_result["resource_id"]

  return redirect(url_for("chat.chat", resource_id=resource_id))

@bp.route('/chat/<resource_id>', methods=["GET"])
@login_required
def chat(resource_id):
  """Show chat UI"""

  # Get session data
  user_id = session.get("user_id")

  # Connect to the db
  db = get_db()

  # Query for sender
  logged_user = db.execute(getUserByIdText(), (user_id,)).fetchone()

  if logged_user is None:
    return render_template("error.html", status=404, message="logged user not found")
  
  # Select participants of the chat
  participants = db.execute(getChatParticipiantsByResourceIdText(), (resource_id,)).fetchone()

  if participants is None:
    return render_template("error.html", status=404, message="Chat room is not found")

  # Select the recipient
  if participants["participant1"] == logged_user["username"]:
    recipient = participants["participant2"]
  else:
    recipient = participants["participant1"]

  # The members of the current chat
  members = {"sender": logged_user["username"], "recipient": recipient}
  
  # Select messages
  messages = db.execute(getMessagesText(), (resource_id,)).fetchall()

  # Convert messages response into a list with dictionaries
  messages_dict = [dict(message) for message in messages]

  return render_template("chat/chat.html", members=members, messages=messages_dict)
