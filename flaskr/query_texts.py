def getUserByIdText():
  return "SELECT id, username FROM users WHERE id=?;"

def getUserByUsernameText():
  return "SELECT id, username FROM users WHERE username=?;"

def searchUserText():
  return "SELECT username FROM users WHERE username LIKE ?;"

def getChatByParticipantsText():
  return """
    SELECT resource_id
    FROM rooms
    WHERE (participant1_id = ? AND participant2_id = ?) OR (participant1_id = ? AND participant2_id = ?);
  """

def getChatParticipiantsByResourceIdText():
  return """
    SELECT 
      (
        SELECT username
        FROM users
        WHERE id = rooms.participant1_id
      ) AS participant1,
      (
        SELECT username
        FROM users
        WHERE id = rooms.participant2_id
      ) AS participant2
    FROM rooms
    WHERE resource_id = ?;
  """

def getMessagesText():
  return """
      SELECT messages.created_at, username, message 
      FROM messages JOIN users ON users.id = messages.author_id 
      WHERE room_id = (SELECT id FROM rooms WHERE resource_id = ?) 
      ORDER BY messages.created_at 
      DESC
    """

def insertChatText():
  return """
    INSERT INTO rooms (resource_id, participant1_id, participant2_id)
    VALUES (?, ?, ?);
  """

def insertMessageText():
  return """
    INSERT INTO messages (created_at, author_id, room_id, message) 
    VALUES (?, ?, 
      (
        SELECT id 
        FROM rooms 
        WHERE resource_id = ?
      ), ?);
  """