from flask import Flask, render_template, request, redirect, url_for
#from utils import mongoUtils
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
@app.route("/home")
def root():
    return render_template("home.html")


@app.route("login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
