#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})


app.run()
