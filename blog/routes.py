from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Post
from flask_login import login_user, logout_user, login_required, current_user  # current user holds info about the current user
from werkzeug.security import generate_password_hash, check_password_hash

# routes is the name of blueprint
routes = Blueprint("routes", __name__)

@routes.route("/")
@routes.route("/home")
def home():
    if current_user.is_authenticated:
        posts = Post.query.all()
        return render_template("home.html", name = current_user, posts = posts)
    else:
        flash('Please sign in first!',category='error')
        return redirect(url_for("routes.login"))

@routes.route("/profile")
def profile():
    return "<h1>Profile</h1>"

@routes.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pass1 = request.form["pass1"]
        user = User.query.filter_by(email=email).first()
        print(user)

        if user:
            if check_password_hash(user.password, pass1):
                login_user(user, remember=True)
                # print(user)
                # print(user.age)
                flash('logged in succesfully',category='success')
                return redirect(url_for("routes.home"))
            else:
                flash('password is not correct!',category='error')
        else:
            flash('User does not exist',category='error')
    return render_template("login.html")

@routes.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        age = request.form["age"]
        gender = request.form["gender"]

        email_exists = User.query.filter_by(email=email).first()
        username_exists =  User.query.filter_by(username=username).first()

        if email_exists:
            flash('email already exists!', category='error')
        elif username_exists:
            flash('username already exists!', category='error')
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

@routes.route("/create-post", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        postTitle = request.form["title"]
        postText = request.form["post"]
        if not postText:
            flash("Please write something!!", category='error')
        elif not postTitle:
            flash("Please provide title to the post!!", category='error')
        else:
            post = Post(user_id=current_user.id, title=postTitle,content=postText)
            db.session.add(post)
            db.session.commit()
            flash("Done :)", category='success')
    return render_template("create_post.html")

@routes.route("/<user>")
def user(user):
    target_user = User.query.filter_by(username=user).first()
    post = Post.query.filter_by(user_id=target_user.id).all() # == posts = User.posts    -> the relationship you made in the model
    return render_template("user.html", user=target_user, posts=post)

@routes.route("/delete-post/<post_id>")
def delete(post_id):
    target_post = Post.query.filter_by(post_id=post_id).first()
    if not target_post:
            flash("Post does not exist.", category='error')
    else:
        db.session.delete(target_post)
        db.session.commit()
        flash("Deleted successfully", category='success')
    return redirect(url_for("routes.home"))


@routes.route("/sign-out")
@login_required # only access if you are loged in
def signout():
    logout_user()
    return redirect(url_for("routes.login"))