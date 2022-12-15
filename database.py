from pymongo import MongoClient

user =  {}

# Establish a connection to mongodb
client = MongoClient("mongodb+srv://mich0803@cluster0.wigqva5.mongodb.net/?retryWrites=true&w=majority")
db = client.user_info
log_db = client.user_history
# Schema 
# username: string
# password: string
# friend_list: string[]

# chat_history
# user_id: string autogenerated by mongo 
# log: string will be split by newline character

# CREATE

# Add a user after registration 
def add_user(username, password):
  # Collection name users 
  user = {
    "username": username,
    "password": password,
    "friend_list": []
  }  
  # Check if user is already existed 
  existed_user = db.users.find_one({"username": username})
  if existed_user == None:
    db.users.insert_one(user) 
    return True
  else:
    return False


def add_history(friend_username, messages):
  print(user)
  if(len(user) == 0):
    print("Please authenticate user first")
  else:
    friend_user = db.users.find_one({"username": friend_username})
    chat_log = {
      "from_id": friend_user["_id"],
      "messages": messages
    }
    log_db.messages.insert_one(chat_log)

# READ

def connect(username):
  global user
  user = db.users.find_one({"username": username})

def retrieve_username():
  return user['username']

def retrieve_friend_list():
  return user["friend_list"]

def retrieve_messages(friend_username):
  friend_user = db.users.find_one({"username": friend_username})
  messages = log_db.messages.find_one({"from_id": friend_user["_id"]})
  print(messages["messages"])

def authenticate(username, password):
  connect(username)
  if user == None:
    return False
  if (user["username"] == username and user["password"] == password):
    return True 
  return False
