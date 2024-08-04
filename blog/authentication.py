"""
This file defines the authentication routes for the Flask application using the 'auth' Blueprint.
It includes endpoints for user login, signup, and logout. The routes handle user authentication,
password hashing, and session management.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from . import db
from .models import User, Post, Comment, Img, Like
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# Define the 'auth' Blueprint for authentication routes
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Endpoint for user login.
    Handles both GET and POST requests. For POST requests, it verifies user credentials,
    logs in the user if valid, and redirects to the home page. If credentials are invalid,
    it flashes an error message.
    """
    if request.method == "POST":
        email = request.form["email"]
        pass1 = request.form["pass1"]
        user = User.query.filter_by(email=email).first()
        print(user)

        if user:
            if check_password_hash(user.password, pass1):
                login_user(user, remember=True)
                flash('Logged in successfully', category='success')
                return redirect(url_for("routes.home"))
            else:
                flash('Password is not correct!', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    """
    Endpoint for user signup.
    Handles both GET and POST requests. For POST requests, it validates the user input,
    checks for existing email or username, hashes the password, creates a new user,
    and logs in the user. It also handles errors and displays appropriate flash messages.
    """
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        age = request.form["age"]
        gender = request.form["gender"]

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email already exists!', category='error')
        elif username_exists:
            flash('Username already exists!', category='error')
        elif pass1 != pass2:
            flash('Passwords are not the same!', category='error')
        elif len(pass1) < 5:
            flash('Password is too short!', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(pass1, method='pbkdf2:sha256'), age=age, gender=gender)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('User Created', category='info')
                login_user(new_user, remember=True)
                return redirect(url_for("routes.home"))
            except Exception as e:
                return f"An error occurred: {e}"
    return render_template("signup.html")

@auth.route("/sign-out")
@login_required
def signout():
    """
    Endpoint for user logout.
    Logs out the current user and redirects to the login page.
    Access is restricted to logged-in users only.
    """
    logout_user()
    return redirect(url_for("auth.login"))
