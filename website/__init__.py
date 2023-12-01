from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy for database interactions
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    
    # Set a secret key for session security
    app.config['SECRET_KEY'] = 'siphumelele'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Set the database URI for SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the database with the Flask app
    db.init_app(app)

    # Import and register blueprints for different parts of the application
    from .admin import admin
    from .user import user
    from .database import User, ReportedIssue
    
    # Create the database if it does not exist
    create_database(app)
    
    # Configure LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # URL to redirect to for login
    login_manager.init_app(app)
    
    # Define how to load a user for Flask-Login
    @login_manager.user_loader 
    def load_user(id):
        return User.query.get(int(id))

    # Register blueprints for different parts of the application
    app.register_blueprint(admin, url_prefix='/') 
    app.register_blueprint(user, url_prefix='/')    

    return app

def create_database(app):
    # Check if the database file exists, if not, create it
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
