from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    User model representing a user in the system.
    Includes fields for email, username, password, age, gender, and date_added.
    Establishes relationships with posts, comments, images, and likes.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(100), nullable=False, unique=True)  # User's email address
    username = db.Column(db.String(100), nullable=False)  # User's username
    password = db.Column(db.String(200), nullable=False)  # User's hashed password
    age = db.Column(db.Integer, nullable=False)  # User's age
    gender = db.Column(db.String(100), nullable=False)  # User's gender
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Date the user was added
    
    # Relationships to access related posts, comments, images, and likes
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    img = db.relationship('Img', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

class Post(db.Model):
    """
    Post model representing a blog post.
    Includes fields for user_id, title, content, and date_created.
    Establishes relationships with comments and likes.
    """
    post_id = db.Column(db.Integer, primary_key=True)  # Primary key for the post
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # Foreign key to User
    title = db.Column(db.String(100), nullable=False)  # Title of the post
    content = db.Column(db.Text, nullable=False)  # Content of the post
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Date the post was created
    
    # Relationships to access related comments and likes
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):
    """
    Comment model representing a comment on a post.
    Includes fields for user_id, post_id, content, and date_created.
    """
    comment_id = db.Column(db.Integer, primary_key=True)  # Primary key for the comment
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # Foreign key to User
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id", ondelete="CASCADE"), nullable=False)  # Foreign key to Post
    content = db.Column(db.Text, nullable=False)  # Content of the comment
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Date the comment was created

class Img(db.Model):
    """
    Img model representing an image uploaded by a user.
    Includes fields for user_id, filename, and filepath.
    """
    img_id = db.Column(db.Integer, primary_key=True)  # Primary key for the image
    userid = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)  # Foreign key to User
    filename = db.Column(db.String(80), unique=True, nullable=False)  # Filename of the image
    filepath = db.Column(db.String(120), nullable=False)  # Filepath to the image

class Like(db.Model):
    """
    Like model representing a like on a post by a user.
    Includes fields for author (user_id) and post_id.
    """
    like_id = db.Column(db.Integer, primary_key=True)  # Primary key for the like
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # Foreign key to User
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete="CASCADE"), nullable=False)  # Foreign key to Post
