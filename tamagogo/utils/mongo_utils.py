from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId
import random

client = MongoClient()
db = client.tamagogo
user_collection = db.users
deed_collection = db.deeds
egg_collection = db.eggs

#The required amount of points per tier of egg
egg_requirements = [-1, 30, 100, 175, 300, 500, 900]


## Getters

def get_user(username):
    return user_collection.find_one({"username": username})

def get_egg(id_string):
    return egg_collection.find_one({"id_string": id_string})

def get_deed(id_num):
    return deed_collection.find_one({"id_num": id_num})



## Auth functions

def hash(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()

def authenticate(username, password):
    user = get_user(username)
    if (user == None):
        return False
    else:
        return user["password"] == hash(username, password)




def check_hatch(username):
    user = get_user(username)
    return user["currScore"] > egg_requirements[get_egg(user["currEgg"])]

def gen_new_egg(username):
    user = get_user(username)
    if user==None:
        return False

    r = random.random()

    if user["totalScore"] < 90:
        return 1
    elif user["totalScore"] < 300:
        if (r < 0.5):
            return 1
        elif (r < 0.78):
            return 2
        else:
            return 3
    else:
        if (r < 0.45):
            return 1
        elif (r < 0.7):
            return 2
        elif (r < 0.9):
            return 3
        elif (r < 0.97):
            return 4
        elif (r < 0.995):
            return 5
        else:
            return 6



## Creation functions

def create_new_user(username, password):
    if (get_user(username) == None):
        user = user_collection.insert(
            {
                "username": username,
                "password": hash(username, password),
                "totalScore": 0,
                "currScore": 0,
                "currEgg": 0,
                "creaturesUnlocked": {}
            }
        )
        return True
    else:
        return False


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
