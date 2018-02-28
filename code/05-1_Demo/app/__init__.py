#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
cors_options = {"supports_credentials": True}
cors = CORS(app, **cors_options)
api = Api(app)

from app import helloworld
