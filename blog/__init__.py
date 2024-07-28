from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ae13200456753159Ae*'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ae13200456*@localhost/Blogdb'

    db.init_app(app)

    from .models import User, Post  # Ensure models are imported

    with app.app_context():
        db.create_all()



    from .routes import routes
    app.register_blueprint(routes, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "routes.login" # if the user is not signed in < direct him to login page
    login_manager.init_app(app)

    # LOGIN MANAGER USES A SESSION TO DETERMINE IF YOU ARE LOGGRD IN OR NOT
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app