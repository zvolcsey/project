from .extensions import socketio
from flask import session, render_template
from flaskr.db import get_db
from flaskr.query_texts import *

@socketio.on("connect")
def handle_connection():
  print("Client connected")


@socketio.on("private_message")
def handle_private_message_event(data):

  # Get session's data
  user_id = session.get("user_id")

  # Conenct the db
  db = get_db()

  # Select the sender's data
  sender_result = db.execute(getUserByIdText(), (user_id,)).fetchone()

  if sender_result is None:
    return render_template("error.html", status=404, message="logged user is not found")
  
  # Select the recipient's data
  recipient_result = db.execute(getUserByUsernameText(), (data["recipient"],)).fetchone()
  
  if recipient_result is None:
    return render_template("error.html", status=404, message="recipient is not found")
  
  # Select the room with the resource id
  room_result = db.execute(getChatParticipiantsByResourceIdText(), (data["chatResourceId"],)).fetchone()

  if room_result is None:
    return render_template("error.html", status=404, message="there is no chat with this resource id")
  
  # Check the participants of the chat
  members = [sender_result["username"], recipient_result["username"]]

  if room_result["participant1"] not in members or room_result["participant2"] not in members:
    return render_template("error.html", status=400, message="the chat has other members")

  # Insert the message to the db
  db.execute(insertMessageText(), (data["date"], user_id, data["chatResourceId"], data["message"],)).fetchone()
  db.commit()

  # Emit the data to the client
  socketio.emit("receive_message", {
    "sender": sender_result["username"],
    "recipient": recipient_result["username"],
    "message_author": sender_result["username"],
    "message": data["message"], 
    "createdAt": data["date"]
    })