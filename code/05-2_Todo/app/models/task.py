#!/usr/bin/env python3

from app import db


class Task(db.Document):
    user_id = db.IntField(required=True)
    task_id = db.StringField(required=True)
    title = db.StringField(required=True, max_length=50)
    description = db.StringField(required=True, max_length=1000)
    done = db.BooleanField(required=True)
    createtime = db.DateTimeField(required=True)
    completetime = db.DateTimeField()

    def to_json(self):
        return {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "createtime": self.createtime.strftime("%Y-%m-%d %H:%M:%S"),
            "completetime": self.completetime.strftime("%Y-%m-%d %H:%M:%S") if self.done else ""
        }
