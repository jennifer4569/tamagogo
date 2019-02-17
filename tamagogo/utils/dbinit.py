from utils import mongo_utils

def create_all_entries():
    mongo_utils.create_egg_entry("default", 1, "undecided")

    mongo_utils.create_deed_entry(1, 1, "Hold the Door", "Hold the door for a friend or a stranger.", "doors")
    mongo_utils.create_deed_entry(2, 2, "Give a Compliment", "Tell someone they have a nice shirt, or that you like their new haircut. Small compliments can go a long way!", "smiles")
    mongo_utils.create_deed_entry(3, 3, "Give Up Your Seat", "Give up your seat on a bus or a train. Even better if its for someone pregnant or elderly!", "times")
    mongo_utils.create_deed_entry(4, 3, "Use a Reusable Bag", "Go shopping with a reusable bag to cut down on plastic waste. It's fashionable and good for the environment!", "times")
    mongo_utils.create_deed_entry(5, 5, "Buy Someone a Coffee", "Or a snack, your coworker or friend will appreciate you for it.", "cups")
    mongo_utils.create_deed_entry(6, 5, "Pick Up Some Litter", "Beautify Earth one step at a time. Even better if you can recycle.", "pieces of garbage")
    mongo_utils.create_deed_entry(7, 10, "Apologize", "Give up an old grudge and apologize for a petty fight. It's not about being right, it's about being friends.", '"sorry"s')
    mongo_utils.create_deed_entry(8, 12, "Use Public Transport", "...instead of driving somewhere. Save the planet one train-ride at a time.", "days")
    mongo_utils.create_deed_entry(9, 15, "Walk/Bike Somewhere", "...instead of driving. As an added bonus, you get a nice cardio workout!", "days")
    mongo_utils.create_deed_entry(10, 15, "Mentor a Collegue/Classmate", "Tutor a classmate, or teach a coworker a neat new trick. Knowledge is power!", "hours")
    mongo_utils.create_deed_entry(11, 16, "Help a Neighbor", "Maybe by mowing their lawn or shovelling their snow. It's easy to cause a good impact in your community.", "times")
    mongo_utils.create_deed_entry(12, 16, "Show Someone Around", "Show a tourist the ins and outs of your city, or give someone directions.", "times")
    mongo_utils.create_deed_entry(13, 22, "Give a Friend a Gift", "...for no particular reason. It's a great way to show someone you appreciate them.", "gifts")
    mongo_utils.create_deed_entry(14, 25, "Give a Generous Tip", "...to really show how much you appreciate someone's service.", "tips")
    mongo_utils.create_deed_entry(15, 30, "Give to Someone in Need", "Give a homeless person a few dollars, or some food. Every little bit counts.", "days made")
    mongo_utils.create_deed_entry(16, 35, "Advocate for Something", "Whether its rights, pride, or beliefs, stand up for something that matters. Join in a parade, or attend a rally, it's up to you how to impact the world!", "events")
    mongo_utils.create_deed_entry(17, 40, "Plant a Tree", "or a bush or some flowers. Save the Earth and beautify your town.", "plants")
    mongo_utils.create_deed_entry(18, 50, "Go Vote", "Exercise your right to vote. Every vote counts!", "votes")
    mongo_utils.create_deed_entry(19, 60, "Donate to Charity", "Sign up to give every month, or donate some old clothes. Giving just one paycheck could change someone's life.", "donations")
    mongo_utils.create_deed_entry(20, 60, "Adopt a Pet", "Give an animal a new loving home.", "animals")
    mongo_utils.create_deed_entry(21, 150, "Sign Up to be an Organ Donor", "Give someone the gift of life.", "times")
    mongo_utils.create_deed_entry(22, 200, "Donate Blood", "The world has a blood shortage, do your part to help someone in need.", "pints of life")

if __name__ == '__main__':
    create_all_entries()
