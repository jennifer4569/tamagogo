from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import mongo_utils
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


#authentication wrapper
def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'uname' not in session:
            flash("Please log in")
            return redirect(url_for("root"))
        else:
            return f(*args, **kwargs)
    return inner


@app.route("/")
def root():
    if "uname" in session:
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if ("username" in request.form and "password" in request.form):
        if (mongo_utils.authenticate(request.form["username"], request.form["password"])):
            user = mongo_utils.get_user(request.form["username"])
            if (user != None):
                session["uname"] = user["username"]
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password")
            return redirect(url_for("root"))
    else:
        return redirect(url_for("root"))


@app.route("/signup", methods=["POST"])
def signup():
    if ("username" in request.form and "password" in request.form):
        if (mongo_utils.create_new_user(request.form["username"], request.form["password"])):
            session["uname"] = mongo_utils.get_user(request.form["username"])["username"]
            return redirect(url_for("home"))
        else:
            flash("That username is already taken")
            return redirect(url_for("root"))
    else:
        return redirect(url_for("root"))


@app.route("/logout")
@require_login
def logout():
    session.pop("uname")


@app.route("/home")
@require_login
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/deeds")
@require_login
def deeds():
    return render_template("deeds.html", deeds = mongo_utils.get_all_deeds())

@app.route("/reward", methods=["POST"])
@require_login
def reward():
    deeds = [(int(each), int(request.form[each])) for each in request.form if request.form[each]]
    user = mongo_utils.get_user(session["uname"])
    for deed in deeds:
        mongo_utils.append_deed(session["uname"], deed)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
