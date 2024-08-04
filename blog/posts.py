"""
This file defines the routes for post-related actions in the Flask application using the 'posts' Blueprint.
It includes endpoints for creating, editing, deleting posts, adding comments, and liking posts.
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

# Define the 'posts' Blueprint for post-related routes
posts = Blueprint("posts", __name__)

@posts.route("/create-post", methods=["GET", "POST"])
@login_required
def create():
    """
    Endpoint to create a new post.
    Handles both GET and POST requests. For POST requests, it validates the input and adds a new post to the database.
    Redirects to the post creation page if successful or flashes an error message if validation fails.
    """
    if request.method == "POST":
        postTitle = request.form["title"]
        postText = request.form["post"]
        if not postText:
            flash("Please write something!!", category='error')
        elif not postTitle:
            flash("Please provide a title for the post!!", category='error')
        else:
            post = Post(user_id=current_user.id, title=postTitle, content=postText)
            db.session.add(post)
            db.session.commit()
            flash("Done :)", category='success')
    return render_template("create_post.html")

@posts.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """
    Endpoint to create a comment on a specific post.
    Handles POST requests to add a comment to a post. Validates that the comment content is provided and adds it to the database.
    Redirects to the home page upon success or flashes an error message if validation fails.
    """
    content = request.form["comment"]
    if not content:
        flash("Please write something!!", category='error')
    else:
        comment = Comment(user_id=current_user.id, post_id=post_id, content=content)
        db.session.add(comment)
        db.session.commit()
        flash("Done :)", category='success')
    referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for("userstemplate.profile"))
    else:
        return redirect(url_for("routes.home"))
    
@posts.route("/delete-comment/<comment_id>")
def comment_delete(comment_id):
    """
    Endpoint to delete a specific comment.
    Deletes the comment from the database if it exists. Redirects to the home page if the referrer URL contains 'profile',
    otherwise redirects to the home page.
    """
    target_comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not target_comment:
        flash("Comment does not exist.", category='error')
    else:
        db.session.delete(target_comment)
        db.session.commit()
        flash("Deleted successfully", category='success')
    referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for("userstemplate.profile"))
    else:
        return redirect(url_for("routes.home"))

@posts.route("/delete-post/<post_id>")
def delete(post_id):
    """
    Endpoint to delete a specific post.
    Deletes the post from the database if it exists. Redirects to the profile page if the referrer URL contains 'profile',
    otherwise redirects to the home page.
    """
    target_post = Post.query.filter_by(post_id=post_id).first()
    if not target_post:
        flash("Post does not exist.", category='error')
    else:
        db.session.delete(target_post)
        db.session.commit()
        flash("Deleted successfully", category='success')
    referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for("userstemplate.profile"))
    else:
        return redirect(url_for("routes.home"))
    


@posts.route("/edit-post/<post_id>", methods=["POST"])
def edit(post_id):
    """
    Endpoint to edit the content of a specific post.
    Updates the post content if the post exists. Redirects to the home page upon success or flashes an error message if the post does not exist.
    """
    target_post = Post.query.filter_by(post_id=post_id).first()
    if not target_post:
        flash("Post does not exist.", category='error')
    else:
        target_post.content = request.form["content"]
        db.session.commit()
        flash("Edited successfully", category='success')
        referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for("userstemplate.profile"))
    else:
        return redirect(url_for("routes.home"))

@posts.route("/like-post/<post_id>")
def like_post(post_id):
    """
    Endpoint to like or unlike a specific post.
    Toggles the like status for the post. Adds a like if it does not exist, or removes it if it does.
    Redirects to the home page after updating the like status.
    """
    liked = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if liked:
        db.session.delete(liked)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for("userstemplate.profile"))
    else:
        return redirect(url_for("routes.home"))
