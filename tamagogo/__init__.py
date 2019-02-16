from flask import Flask, render_template, request, redirect, url_for
from utils import mongo_utils
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


#authentication wrapper
def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        print(session)
        if 'uid' not in session:
            flash("Please log in")
            return redirect(url_for("root"))
        else:
            return f(*args, **kwargs)
    return inner


@app.route("/")
def root():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if ("username" in request.form and "password" in request.form):
        if (mongo_utils.authenticate(request.form["username"], request.form["password"])):
            user = mongo_utils.get_user(username)
            if (user != None):
                session["uid"] = user["_id"]
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password")
            return redirect(url_for("root"))
    else:
        return redirect(url_for("root"))


@app.route("/signup", methods=["POST"])
def signup():
    if ("username" in request.form and "password" in request.form):
        user = mongo_utils.create_new_user(username, password)
        if (user != None):
            session["uid"] = user["_id"]
            return redirect(url_for("home"))
        else:
            flash("That username is already taken")
            return redirect(url_for("root"))
    else:
        return redirect(url_for("root"))


@app.route("/logout")
@require_login
def logout():
    session.pop("user_auth")


@app.route("/home")
@require_login
def home():
    return render_template("home")

@app.route("/about")
def about():
    return render_template("about")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
