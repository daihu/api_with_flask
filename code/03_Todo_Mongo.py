#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

from datetime import datetime
import shortuuid


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'todo',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


class Task(db.Document):
    task_id = db.StringField(required=True)
    title = db.StringField(required=True, max_length=50)
    description = db.StringField(required=True, max_length=1000)
    done = db.BooleanField(required=True)
    createtime = db.DateTimeField(required=True)
    completetime = db.DateTimeField()

    def to_json(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "createtime": self.createtime.strftime("%Y-%m-%d %H:%M:%S"),
            "completetime": self.completetime.strftime("%Y-%m-%d %H:%M:%S") if self.done else ""
        }


@app.route('/todo/task', methods=['POST'])
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'Request not Json or miss task.'})
    else:
        task = Task(
            task_id=shortuuid.uuid(),
            title=request.json['task'],
            description=request.json['description'] if 'decription' in request.json else "",
            done=False,
            createtime=datetime.now()
        )
        task.save()
    return jsonify({'status': 0, 'task_id': task['task_id']})


@app.route('/todo/task/<task_id>', methods=['GET'])
def getTask(task_id):
    task = Task.objects(task_id=task_id).first()
    if not task:
        return jsonify({'err': 'Not found.'})
    else:
        return jsonify({'status': 0, 'task': task.to_json()})


@app.route('/todo/tasks', methods=['GET'])
def getTasks():
    tasks = Task.objects()
    return jsonify({'status': 0, 'tasks': [task.to_json() for task in tasks]})


@app.route('/todo/task/<task_id>', methods=['PUT'])
def putTask(task_id):
    task = Task.objects(task_id=task_id).first()
    if not task:
        return jsonify({'err': 'Not found.'})
    else:
        if 'task' in request.json:
            task.update(title=request.json['task'])
        if 'description' in request.json:
            task.update(description=request.json['description'])
        if 'done' in request.json:
            if request.json['done'] == True:
                task.update(done=True, completetime=datetime.now())
        task = Task.objects(task_id=task_id).first()
        return jsonify({'status': 0, 'task': task.to_json()})


@app.route('/todo/task/<task_id>', methods=['DELETE'])
def deleteTask(task_id):
    task = Task.objects(task_id=task_id).first()
    if not task:
        return jsonify({'err': 'Not found.'})
    else:
        task.delete()
        return jsonify({'status': 0, 'task_id': task['task_id']})


if __name__ == '__main__':
    app.run(debug=True)
