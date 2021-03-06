from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId
import datetime
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

def get_requirement(i):
    return egg_requirements[i]

def get_all_deeds():
    return sorted([deed for deed in deed_collection.find()], key = lambda x: x["worth"])


## Auth functions

def hash(username, password):
    return sha256(str(username+password).encode('utf-8')).hexdigest()

def authenticate(username, password):
    user = get_user(username)
    if (user == None):
        return False
    else:
        return user["password"] == hash(username, password)


def do_hatch(username):
    user = get_user(username)
    curr_egg = get_egg(user["currEgg"])
    cname = curr_egg["cname"]
    user_collection.update_one({"username": username}, {"$inc": {"currScore": -1 * egg_requirements[curr_egg["rarity"]]}})
    creature_dict = user["creaturesUnlocked"]
    if cname not in creature_dict:
        creature_dict[cname] = 1
    else:
        creature_dict[cname] += 1
    user_collection.update_one({"username": username}, {"$set": {"creaturesUnlocked": creature_dict}})
    return gen_new_egg(username)

def check_hatch(username):
    user = get_user(username)
    return user["currEgg"] == "" or user["currScore"] >= egg_requirements[get_egg(user["currEgg"])["rarity"]]

def gen_new_egg_tier(username):
    user = get_user(username)
    if user==None:
        return 0

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

def gen_new_egg(username):
    tier = gen_new_egg_tier(username)
    egg_list = [egg for egg in egg_collection.find({"rarity": tier})]
    new_egg = random.choice(egg_list)["id_string"]
    user_collection.update_one({"username": username}, {"$set": {"currEgg": new_egg}})
    return new_egg


def append_deed(username, deedinfo):
    print(username)
    user = get_user(username)
    deed = get_deed(deedinfo[0])
    points = deed["worth"] * deedinfo[1]
    new_hist = user["history"] + [(deedinfo[0], deedinfo[1], str(datetime.date.today()))]
    user_collection.update_one({"username": username}, {"$set": {"history": new_hist}})
    user_collection.update_one({"username": username}, {"$inc": {"currScore": points, "totalScore": points}})
    total_hatches = [0,0,0,0,0,0]
    while (check_hatch(username)):
        egg = do_hatch(username)
        total_hatches[get_egg(egg)["rarity"]-1] += 1
    return total_hatches


def get_all_creature_info(username):
    user = get_user(username)
    creature_dict = user["creaturesUnlocked"]
    creatures_list = [[],[],[],[],[],[]]
    for creature in creature_dict:
        egg = egg_collection.find_one({"cname": creature})
        temp_dic = {}
        temp_dic["name"] = creature.capitalize()
        temp_dic["creature_img"] = creature
        temp_dic["count"] = creature_dict[creature]
        temp_dic["egg_img"] = egg["id_string"]

        creatures_list[egg["rarity"]-1].append(temp_dic)
    print(creatures_list)
    return creatures_list

## Creation functions

def create_new_user(username, password):
    if (get_user(username) == None):
        user_collection.insert(
            {
                "username": username,
                "password": hash(username, password),
                "totalScore": 0,
                "currScore": 0,
                "currEgg": "",
                "creaturesUnlocked": {},
                "history": []
            }
        )
        gen_new_egg(username)
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
