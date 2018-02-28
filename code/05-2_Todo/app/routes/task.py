#!/usr/bin/env python3

from app import app

from flask import jsonify, request
from flask_login import current_user, login_required

from app.models.task import Task

from datetime import datetime
import shortuuid


@app.route('/todo/task', methods=['POST'])
@login_required
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'Request not Json or miss task.'})
    else:
        task = Task(
            user_id=current_user.user_id,
            task_id=shortuuid.uuid(),
            title=request.json['task'],
            description=request.json['description'] if 'decription' in request.json else "",
            done=False,
            createtime=datetime.now()
        )
        task.save()
    return jsonify({'status': 0, 'task_id': task['task_id']})


@app.route('/todo/task/<task_id>', methods=['GET'])
@login_required
def getTask(task_id):
    task = Task.objects(user_id=current_user.user_id, task_id=task_id).first()
    if not task:
        return jsonify({'err': 'Not found.'})
    else:
        return jsonify({'status': 0, 'task': task.to_json()})


@app.route('/todo/tasks', methods=['GET'])
@login_required
def getTasks():
    tasks = Task.objects(user_id=current_user.user_id)
    return jsonify({'status': 0, 'tasks': [task.to_json() for task in tasks]})


@app.route('/todo/task/<task_id>', methods=['PUT'])
@login_required
def putTask(task_id):
    task = Task.objects(user_id=current_user.user_id, task_id=task_id).first()
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
@login_required
def deleteTask(task_id):
    task = Task.objects(user_id=current_user.user_id, task_id=task_id).first()
    if not task:
        return jsonify({'err': 'Not found.'})
    else:
        task.delete()
        return jsonify({'status': 0, 'task_id': task['task_id']})
