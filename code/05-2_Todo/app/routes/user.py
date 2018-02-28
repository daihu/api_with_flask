#!/usr/bin/env python3

from app import app

from flask import jsonify, request
from flask_login import current_user, login_required

from app.models.user import User


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
