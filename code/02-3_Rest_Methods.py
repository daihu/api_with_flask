#!/usr/bin/env python3

from flask import Flask, jsonify, request


app = Flask(__name__)

tasks = ["Hello World"]


@app.route('/task', methods=['GET'])
def getTask():
    return jsonify({'tasks': tasks})


@app.route('/task', methods=['POST'])
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'miss task'})
    tasks.append(request.json['task'])
    return jsonify({'tasks': tasks})


@app.route('/task', methods=['PUT'])
def resetTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'miss task'})
    tasks[:] = []
    tasks.append(request.json['task'])
    return jsonify({'tasks': tasks})


@app.route('/task', methods=['DELETE'])
def deleteTask():
    tasks[:] = []
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)
