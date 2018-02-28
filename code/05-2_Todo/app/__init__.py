#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
cors_options = {"supports_credentials": True}
cors = CORS(app, **cors_options)
api = Api(app)

app.config.from_object('dev')

db = MongoEngine()
db.init_app(app)

# login_manager & load_user
login_manager = LoginManager()
login_manager.init_app(app)

from app.models.user import User
@login_manager.user_loader
def load_user(user_id):
    return User.objects(user_id=user_id).first()

# Import routes
from app.routes import auth
from app.routes import user
from app.routes import task
