from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'siphumelele'

    # Import and register blueprints for different parts of the application
    from .admin import admin
    from .user import user

    app.register_blueprint(admin, url_prefix='/') 
    app.register_blueprint(user, url_prefix='/')    

    return app
