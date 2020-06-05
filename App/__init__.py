from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from App.config import Config


db=SQLAlchemy()
bcrypt=Bcrypt()

login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='flash-unsuccess'


mail = Mail()




def create_app(config_class=Config):
    app=Flask(__name__,template_folder='templates',static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from App.users.routes import users
    from App.posts.routes import posts
    from App.main.routes import main
    from App.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app