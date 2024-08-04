"""
This file defines the routes for general application actions in the Flask application using the 'routes' Blueprint.
It includes endpoints for the home page, statistics, and visualizations of user data.
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

# Define the 'routes' Blueprint for general routes
routes = Blueprint("routes", __name__)

@routes.route("/")
@routes.route("/home")
def home():
    """
    Endpoint for the home page.
    Displays posts and comments if the user is authenticated.
    Redirects to the login page if the user is not authenticated.
    """
    if current_user.is_authenticated:
        posts = Post.query.all()  # Fetch all posts
        comments = Comment.query.all()  # Fetch all comments
        return render_template("home.html", name=current_user, posts=posts, comments=comments)
    else:
        flash('Please sign in first!', category='error')
        return redirect(url_for("auth.login"))

@routes.route("/statistics")
def statistics():
    """
    Endpoint for generating and displaying various statistical data.
    Creates and saves plots for post counts by user, gender distribution, and most liked posts.
    Renders the statistics page with the generated data.
    """
    # Query for the number of posts per user
    mostposts = db.session.query(User.username, Post.user_id, func.count(Post.post_id).label('Post Count'))\
                          .join(Post, User.id == Post.user_id)\
                          .group_by(Post.user_id)\
                          .order_by(func.count(Post.post_id).desc()).all()
    
    # Prepare data for post count histogram
    usernames = [item[0] for item in mostposts]
    counts = [item[2] for item in mostposts]
    
    plt.figure(figsize=(10, 6))
    plt.hist(counts, color='blue', edgecolor='black')
    plt.title('Post Counts by User')
    plt.ylabel('No. of Users')
    plt.xlabel('Post Count')
    plt.tight_layout()
    
    # Save the histogram to a file
    filepath = os.path.join(current_app.config['STATIC_FOLDER'], 'photos/statistical_photos/posts_count_distribution.png')
    if os.path.exists(filepath):
        os.remove(filepath)
    plt.savefig(filepath)
    plt.close()

    # Query for gender distribution
    genders = db.session.query(User.gender, func.count(User.id).label('Gender Count'))\
                        .group_by(User.gender).all()
    if not genders:
        genders = [('Unknown', 0)]  # Handle empty case if needed

    counts = [item[1] for item in genders]
    my_data = counts + [0] * (3 - len(counts))  # Pad with zeros if there are fewer than 3 items
    my_labels = ["Males", "Females", "Other"]
    
    plt.figure(figsize=(8, 8))
    plt.pie(my_data, labels=my_labels, autopct="%1.1f%%")
    plt.title("Gender Distribution")
    plt.tight_layout()
    
    # Save the pie chart to a file
    filepath = os.path.join(current_app.config['STATIC_FOLDER'], 'photos/statistical_photos/gender_distribution.png')
    if os.path.exists(filepath):
        os.remove(filepath)
    plt.savefig(filepath)
    plt.close()

    # Query for the most liked posts
    most_liked_posts = db.session.query(Like.post_id, Post.title, User.username, func.count(Like.like_id))\
                                .join(Post, Like.post_id == Post.post_id)\
                                .join(User, Post.user_id == User.id)\
                                .group_by(Like.post_id)\
                                .order_by(func.count(Like.like_id).desc())\
                                .limit(10).all()

    return render_template("statistics.html", mostposts=mostposts, gender=genders, count=counts, most_liked_posts=most_liked_posts)
