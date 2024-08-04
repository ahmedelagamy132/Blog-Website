"""
This file defines the routes related to user profiles and user management in the Flask application using the 'userstemplate' Blueprint.
It includes endpoints for viewing and updating user profiles, listing users, and uploading profile pictures.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from . import db
from .models import User, Post, Comment, Img, Like
from flask_login import login_user, logout_user, login_required, current_user  # current user holds info about the current user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# Define the 'userstemplate' Blueprint for user-related routes
userstemplate = Blueprint("userstemplate", __name__)

@userstemplate.route("/profile")
@login_required
def profile():
    """
    Endpoint to display the current user's profile.
    Retrieves and renders the current user's profile information, including posts and profile image.
    """
    img = Img.query.filter_by(userid=current_user.id).first()
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", user=current_user, img=img, posts=posts)


@userstemplate.route("/<user>")
def user(user):
    """
    Endpoint to display a specific user's profile based on the username.
    Retrieves and renders the user's profile information, including posts and profile image.
    Returns a 404 error if the user is not found.
    """
    target_user = User.query.filter_by(username=user).first()
    
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    posts = Post.query.filter_by(user_id=target_user.id).all()
    img = Img.query.filter_by(userid=target_user.id).first()        
    return render_template("user.html", user=target_user, posts=posts, img=img)


@userstemplate.route("/users")
def users():
    """
    Endpoint to display a list of all users.
    Retrieves and renders a list of all registered users.
    """
    users = User.query.all()
    return render_template("users_list.html", users=users)

@userstemplate.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    Endpoint to upload a profile picture for the current user.
    Handles file uploads, saves the file, and updates the user's profile image.
    Deletes any existing profile image before saving the new one.
    """
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(url_for("userstemplate.profile"))
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "profile_pictures", filename)

    # Remove existing image if it exists
    existing_user_img = Img.query.filter_by(userid=current_user.id).first()
    if existing_user_img:
        db.session.delete(existing_user_img)
        db.session.commit()

    file.save(file_path)
    img = Img(userid=current_user.id, filename=filename, filepath=file_path)
    db.session.add(img)
    db.session.commit()
    flash("Uploaded successfully", category='success')
    return redirect(url_for("userstemplate.profile"))

@userstemplate.route("/update", methods=["POST"])
@login_required
def update():
    """
    Endpoint to update the current user's profile information.
    Updates user details such as email, username, password, age, and gender.
    Validates the input and checks for existing email and username.
    """
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["pass1"]
    password2 = request.form["pass2"]
    age = request.form["age"]
    gender = request.form["gender"]

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    if email_exists:
        flash('Email already exists!', category='error')
    elif username_exists:
        flash('Username already exists!', category='error')
    elif password != password2:
        flash('Passwords are not the same!', category='error')
    elif len(password) < 5:
        flash('Password is too short!', category='error')
    else:
        try:
            current_user.email = email
            current_user.username = username
            current_user.password = generate_password_hash(password, method='pbkdf2:sha256')  # Hash the new password
            current_user.age = age
            current_user.gender = gender
            db.session.commit()
            flash('Profile updated successfully', category='info')
        except Exception as e:
            return f"An error occurred: {e}"
    return redirect(url_for("userstemplate.profile"))
