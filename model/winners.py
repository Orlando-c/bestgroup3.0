""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table username is plural, class username is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=False, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _score = db.Column(db.Integer, primary_keys=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, username, id, password="123qwerty", score):
        self._username = username    # variables with self prefix become part of the object, 
        self._id = id
        self.set_password(password)
        self._score = score

    # a username getter method, extracts username from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows username to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username
    
    # a getter method, extracts email from object
    @property
    def id(self):
        return self._id
    
    # a setter function, allows username to be updated after initial object creation
    @id.setter
    def id(self, id):
        self._id = id
        
    # check if id parameter matches user id in object, return boolean
    def is_id(self, id):
        return self._id == id
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # score property is returned as string, to avoid unfriendly outcomes
    @property
    def score(self):
        score_string = self._score
        return score_string
    
    # score should be have verification for type date
    @score.setter
    def score(self, score):
        self._score = score
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "id": self.password,
            "score": self.score,
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user username, password, phone
    # returns self
    def update(self, username="", id="", password=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(id) > 0:
            self.id = id
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = User(username='Thomas Edison', id='toby', password='123toby', score=date(1847, 2, 11))
        u2 = User(username='Nicholas Tesla', id='niko', password='123niko')
        u3 = User(username='Alexander Graham Bell', id='lex', password='123lex')
        u4 = User(username='Eli Whitney', id='whit', password='123whit')
        u5 = User(username='John Mortensen', id='jm1021', score=date(1959, 10, 21))

        users = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.username + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.id}")
            