from pymongo import MongoClient
from hashlib import sha256


client = MongoClient()
db = client.tamagogo
collection = db.users


def create_new_user(username, password):
    if (get_user(username) == None):
        user = collection.insert(
            {
                "username": username,
                "password": hash(username, password),
                "totalScore": 0,
                "currScore": 0,
                "creaturesUnlocked": {}
            }
        )
        return user
    else:
        return None

def get_user(username):
    return collection.find_one({"username": username})

def hash(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()

def authenticate(username, password):
    user = get_user(username)
    if (user == None):
        return False
    else:
        return user["password"] == hash(username, password)
