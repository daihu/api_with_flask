#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

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

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'secret_key'


class User(db.Document):
    user_id = db.StringField(required=True)
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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(user_id=user_id).first()


@app.route('/register', methods=['POST'])
def registerUser():
    if not request.json or not 'name' in request.json or not 'pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss name/pwd'})
    elif User.objects(name=request.json['name']).first():
        return jsonify({'err': 'Name is already existed.'})
    else:
        user = User(
            user_id=shortuuid.uuid(),
            name=request.json['name'],
            email=request.json['email'] if 'email' in request.json else "",
            pwd=request.json['pwd'],
            createtime=datetime.now()
        )
        try:
            user.save()
            login_user(user)
        except Exception as e:
            print (e)
            return jsonify({'err': 'Register error.'})
    return jsonify({'status': 0, 'user_id': user['user_id'], 'msg': 'Register success.'})


@app.route('/login', methods=['POST'])
def login():
    if not request.json or not 'name' in request.json or not 'pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss name/pwd'})
    else:
        user = User.objects(
            name=request.json['name'], pwd=request.json['pwd']).first()
    if user:
        login_user(user)
        return jsonify({'status': 0, 'user_id': user.get_id(), 'msg': 'Login success.'})
    else:
        return jsonify({'err': 'Login fail.'})


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'status': 0, 'msg': 'Logout success.'})


@app.route('/user', methods=['GET'])
def getUser():
    if current_user.is_authenticated:
        return jsonify({'status': 0, 'user': current_user.to_json()})
    else:
        return jsonify({'err': 'Not login.'})


@app.route('/user/email', methods=['PUT'])
@login_required
def putUserEmail():
    if not request.json or not 'email' in request.json:
        return jsonify({'err': 'Request not Json or miss email'})
    else:
        current_user.email = request.json['email']
        try:
            current_user.save()
        except Exception:
            return jsonify({'err': 'Modify email error.'})
        return jsonify({'status': 0, 'msg': 'Email has been modified.', 'user': current_user.to_json()})


@app.route('/user/pwd', methods=['PUT'])
@login_required
def putUserPWD():
    if not request.json or not 'current_pwd' in request.json or not 'new_pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss current_pwd/new_pwd'})
    else:
        current_pwd = current_user.pwd
    if not request.json['current_pwd'] == current_pwd:
        return jsonify({'err': 'current_pwd is not right.'})
    else:
        current_user.pwd = request.json['new_pwd']
        try:
            current_user.save()
        except Exception:
            return jsonify({'err': 'Modify PWD error.'})
        return jsonify({'status': 0, 'msg': 'PWD has been modified.', 'user_id': current_user.user_id})


if __name__ == '__main__':
    app.run(debug=True)
