#!/usr/bin/env python3

from flask import Flask, jsonify, request


app = Flask(__name__)

tasks = [
    {
        'task_id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'task_id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/tasks', methods=['GET'])
def getTasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/task/<int:task_id>', methods=['GET'])
def getTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        return jsonify({'task': task[0]})


@app.route('/todo/task', methods=['POST'])
def postTask():
    if not request.json or not 'task' in request.json:
        return jsonify({'err': 'Request not Json or miss task.'})
    else:
        task = {
            # ！实际开发不适用，获取tasks最后一个的task_id+1作为新增task的task_id
            'task_id': tasks[-1]['task_id'] + 1,
            'title': request.json['task'],
            'description': request.json.get('description', ""),
            'done': False
        }
    tasks.append(task)
    return jsonify({'status': 0, 'task_id': task['task_id']})


@app.route('/todo/task/<int:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        tasks.remove(task[0])
        return jsonify({'status': 0, 'task_id': task_id, 'msg': 'Deleted.'})


@app.route('/todo/task/<int:task_id>', methods=['PUT'])
def putTask(task_id):
    task = list(filter(lambda t: t['task_id'] == task_id, tasks))
    if len(task) == 0:
        return jsonify({'err': 'Not found.'})
    else:
        if 'task' in request.json:
            task[0]['task'] = request.json['task']
        if 'description' in request.json:
            task[0]['description'] = request.json['description']
        if 'done' in request.json:
            if request.json['done'] == True:
                task[0]['done'] = request.json['done']
        return jsonify({'status': 0, 'task': task[0]})


if __name__ == '__main__':
    app.run(debug=True)
