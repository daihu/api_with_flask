#!/usr/bin/env python3

from app import db


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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
