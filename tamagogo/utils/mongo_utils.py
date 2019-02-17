from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId


client = MongoClient()
db = client.tamagogo
user_collection = db.users
deed_collection = db.deeds
egg_collection = db.eggs

#The required amount of points per tier of egg
egg_requirements = [-1, 30, 100, 175, 300, 500, 900]


def create_new_user(username, password):
    if (get_user(username) == None):
        user = user_collection.insert(
            {
                "username": username,
                "password": hash(username, password),
                "totalScore": 0,
                "currScore": 0,
                "currEgg": None,
                "creaturesUnlocked": {}
            }
        )
        return True
    else:
        return False

def get_user(username):
    return user_collection.find_one({"username": username})

def hash(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()

def authenticate(username, password):
    user = get_user(username)
    if (user == None):
        return False
    else:
        return user["password"] == hash(username, password)

def check_hatch(username):
    return get_user["currScore"] > 0

def gen_new_egg(username):
    user = get_use(username)
    if user==None:
        return False
    if user["totalScore"] < 90:
        pass
    elif user["totalScore"] < 300:
        pass
    else:
        pass


def create_egg_entry(id_string, rarity, cname):
    if (egg_collection.find_one({"id_string": id_string}) != None):
        return False
    egg_collection.insert({
        "id_string": id_string,
        "rarity": rarity,
        "cname": cname
    })
    return True

def create_deed_entry(id_num, worth, text, desc, units):
    if (deed_collection.find_one({"id_num": id_num}) != None):
        return False
    deed_collection.insert({
        "id_num": id_num,
        "worth": worth,
        "text": text,
        "desc": desc,
        "units": units
    })
    return True
