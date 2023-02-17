from random import randrange
from datetime import date
import os
import base64
import json

from app import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Player(db.Model):
    __tablename__ = 'fables'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    userstory = db.Column(db.String(255), unique=False, nullable=False)
    aistory = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, username, userstory, aistory):
        self.username = username
        self.userstory = userstory
        self.aistory = aistory

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def userstory(self):
        return self._userstory

    @userstory.setter
    def userstory(self, userstory):
        self._userstory = userstory

    @property
    def aistory(self):
        return self._aistory

    @aistory.setter
    def aistory(self, aistory):
        self._aistory = aistory

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "user-story": self.userstory,
            "AI-story": self.aistory,
        }

    def update(self, username="", userstory=""):
        if len(username) > 0:
            self.username = username
        if len(userstory) > 0:
            self.userstory = userstory
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initFables():
    db.create_all()

initFables()