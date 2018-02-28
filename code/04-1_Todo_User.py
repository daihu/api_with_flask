#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

from datetime import datetime


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'todo',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


class User(db.Document):
    user_id = db.IntField(required=True)
    name = db.StringField(required=True, max_length=100)
    email = db.StringField(max_length=200)
    pwd = db.StringField(requied=True, min_length=6)
    createtime = db.DateTimeField(required=True)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }


@app.route('/user', methods=['POST'])
def postUser():
    if not request.json or not 'name' in request.json or not 'pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss name or pwd'})
    elif User.objects(name=request.json['name']).first():
        return jsonify({'err': 'Name is already existed.'})
    else:
        try:
            user = User(
                user_id=User.objects().count() + 1,
                name=request.json['name'],
                email=request.json['email'] if 'email' in request.json else "",
                pwd=request.json['pwd'],
                createtime=datetime.now()
            )
            user.save()
        except Exception as e:
            return jsonify({'err': 'Save Error. Please check your input length: pwd>6, name<100, email<200.'})
    return jsonify({'status': 0, 'user_id': user['user_id']})


@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = User.objects(user_id=user_id).first()
    if not user:
        return jsonify({'err': 'Not found.'})
    else:
        return jsonify({'status': 0, 'user': user.to_json()})


if __name__ == '__main__':
    app.run(debug=True)