#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Flask',
        'description': 'Simple Demo',
        'done': False
    }
]


@app.route('/<int:task_id>', methods=['GET'])
def index(task_id):
    return jsonify({'task': tasks[task_id-1]})


if __name__ == '__main__':
    app.run(debug=True)
