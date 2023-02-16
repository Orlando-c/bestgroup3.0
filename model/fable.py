""" database dependencies to support sqliteDB examples """

import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Responses(db.Model):
    __tablename__ = 'responses'  # table name is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=True, nullable=False)
    _aibody = db.Column(db.String(255), unique=False, nullable=False)
    _userbody = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, title, text, imageURL):
        self._username = title
        self._aibody = text
        self._userbody = imageURL

    @property
    def username(self):
        return self._username
  
    @username.setter
    def username(self, title):
        self._username = title
  
    @property
    def aibody(self):
        return self._aibody
  
    @aibody.setter
    def aibody(self, text):
        self._aibody = text
  
    @property
    def userbody(self):
        return self._userbody
  
    @userbody.setter
    def userbody(self, imageURL):
        self._userbody = imageURL

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "Username": self._username,
            "AI Body": self._aibody,
            "User Body": self._userbody
        }
  
    def update(self, title="", text="", imageURL=""):
        if len(title) > 0:
            self._username = title
        if len(text) > 0:
            self._aibody = text
        if len(imageURL) > 0:
            self._userbody = imageURL
        db.session.commit()
        return self

    def delete(self):
        db.session.commit()
        db.session.delete(self)
        return None


def initUsers():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        u1 = Responses(title="New York City", text="Fortnite", imageURL="amomh.com")
        u2 = Responses(title="S", text="Among", imageURL="fort.com")
        users = [u1, u2]
        for user in users:
            try:
                user.create()
            except IntegrityError:
                db.session.remove()
                print(f"Duplicate or error: {user._username}")