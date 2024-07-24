from flask import Blueprint, render_template, redirect, url_for

# routes is the name of blueprint
routes = Blueprint("routes", __name__)

@routes.route("/")
@routes.route("/home")
def home():
    return render_template("base.html", name = "Tim")

@routes.route("/profile")
def profile():
    return "<h1>Profile</h1>"

@routes.route("/login")
def login():
    return render_template("login.html")

@routes.route("/sign-up")
def signup():
    return render_template("signup.html")

@routes.route("/sign-out")
def signout():
    return redirect(url_for("routes.home"))