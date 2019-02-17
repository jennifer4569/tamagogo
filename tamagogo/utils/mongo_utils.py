from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId
import random

client = MongoClient()
db = client.tamagogo
user_collection = db.users
deed_collection = db.deeds
egg_collection = db.eggs


## Useful constants

#The required amount of points per tier of egg
egg_requirements = [-1, 30, 100, 175, 300, 500, 900]


## Getters

def get_user(username):
    return user_collection.find_one({"username": username})

def get_egg(id_string):
    return egg_collection.find_one({"id_string": id_string})

def get_deed(id_num):
    return deed_collection.find_one({"id_num": id_num})

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



def check_hatch(username):
    user = get_user(username)
    return user["currScore"] > egg_requirements[get_egg(user["currEgg"])]

def gen_new_egg_tier(username):
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


def create_all_entries():
    deed_collection.drop()

    create_egg_entry("default", 1, "undecided")

    create_deed_entry(1, 1, "Hold the Door", "Hold the door for a friend or a stranger.", "doors")
    create_deed_entry(2, 2, "Give a Compliment", "Tell someone they have a nice shirt, or that you like their new haircut. Small compliments can go a long way!", "smiles")
    create_deed_entry(3, 3, "Give Up Your Seat", "Give up your seat on a bus or a train. Even better if its for someone pregnant or elderly!", "times")
    create_deed_entry(4, 3, "Use a Reusable Bag", "Go shopping with a reusable bag to cut down on plastic waste. It's fashionable and good for the environment!", "times")
    create_deed_entry(5, 5, "Buy Someone a Coffee", "Or a snack, your coworker or friend will appreciate you for it.", "cups")
    create_deed_entry(6, 5, "Pick Up Some Litter", "Beautify Earth one step at a time. Even better if you can recycle.", "pieces")
    create_deed_entry(7, 10, "Apologize", "Give up an old grudge and apologize for a petty fight. It's not about being right, it's about being friends.", '"sorry"s')
    create_deed_entry(8, 12, "Use Public Transport", "...instead of driving somewhere. Save the planet one train-ride at a time.", "days")
    create_deed_entry(9, 15, "Walk/Bike Somewhere", "...instead of driving. As an added bonus, you get a nice cardio workout!", "days")
    create_deed_entry(10, 15, "Mentor a Colleague/Classmate", "Tutor a classmate, or teach a coworker a neat new trick. Knowledge is power!", "hours")
    create_deed_entry(11, 16, "Help a Neighbor", "Maybe by mowing their lawn or shovelling their snow. It's easy to cause a good impact in your community.", "times")
    create_deed_entry(12, 16, "Show Someone Around", "Show a tourist the ins and outs of your city, or give someone directions.", "times")
    create_deed_entry(13, 22, "Give a Friend a Gift", "...for no particular reason. It's a great way to show someone you appreciate them.", "gifts")
    create_deed_entry(14, 25, "Give a Generous Tip", "...to really show how much you appreciate someone's service.", "tips")
    create_deed_entry(15, 30, "Give to Someone in Need", "Give a homeless person a few dollars, or some food. Every little bit counts.", "smiles")
    create_deed_entry(16, 35, "Advocate for Something", "Whether its rights, pride, or beliefs, stand up for something that matters. Join in a parade, or attend a rally, it's up to you how to impact the world!", "events")
    create_deed_entry(17, 40, "Plant a Tree", "or a bush or some flowers. Save the Earth and beautify your town.", "plants")
    create_deed_entry(18, 50, "Go Vote", "Exercise your right to vote. Every vote counts!", "votes")
    create_deed_entry(19, 60, "Donate to Charity", "Sign up to give every month, or donate some old clothes. Giving just one paycheck could change someone's life.", "donations")
    create_deed_entry(20, 60, "Adopt a Pet", "Give an animal a new loving home.", "animals")
    create_deed_entry(21, 150, "Sign Up to be an Organ Donor", "Give someone the gift of life.", "times")
    create_deed_entry(22, 200, "Donate Blood", "The world has a blood shortage, do your part to help someone in need.", "pints")

if __name__ == '__main__':
    create_all_entries()
