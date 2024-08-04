"""
This file contains the application factory function for creating a Flask application instance.
It configures the application with necessary settings, initializes extensions such as SQLAlchemy
and Flask-Login, sets up the database connection, and registers blueprints for various parts of
the application including routes, posts, APIs, authentication, and user management.

It also includes error handling for database connection issues and defines a user loader function
for user authentication.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import time
from sqlalchemy.exc import OperationalError
import os
# Initialize SQLAlchemy and LoginManager instances
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)
    
    # Application configuration settings
    app.config['SECRET_KEY'] = 'Ae13200456753159Ae*'  # Secret key for session management
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ae13200456*@localhost/Blogdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ae13200456*@db/Blogdb'  # Database URI for SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size for uploads (16 MB)
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  # Allowed image file extensions
    app.config['UPLOAD_FOLDER'] = r'C:\Users\ahmed\Desktop\Blog\blog\static\photos'  # Directory for uploaded files
    app.config['STATIC_FOLDER'] = os.path.join(app.root_path, 'static')


    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Post, Comment, Img, Like
    
    # Retry database connection in case of failure
    retries = 5
    while retries:
        try:
            with app.app_context():
                db.create_all()  # Create database tables if they do not exist
            break
        except OperationalError:
            retries -= 1
            print('Database connection failed, retrying...')
            time.sleep(5)  # Wait before retrying
    
    # Import and register Blueprints for different parts of the application
    from .routes import routes
    app.register_blueprint(routes, url_prefix="/")

    from .posts import posts
    app.register_blueprint(posts, url_prefix="/")

    from .apis import apis
    app.register_blueprint(apis, url_prefix="/")

    from .authentication import auth
    app.register_blueprint(auth, url_prefix="/")

    from .user import userstemplate
    app.register_blueprint(userstemplate, url_prefix="/")

    # Configure and initialize the LoginManager
    login_manager.login_view = "routes.login"  # Redirect to login page if user is not authenticated
    login_manager.init_app(app)

    # Define a user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Load a user by ID

    return app
