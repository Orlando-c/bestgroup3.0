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
class Player(db.Model):
    __tablename__ = 'fables'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=True, nullable=False)
    _userstory = db.Column(db.String(255), unique=False, nullable=False)
    _aistory = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, userstory, aistory):
        self._username = name    # variables with self prefix become part of the object, 
        self._userstory = userstory
        self._aistory = aistory

    # a name getter method, extracts name from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._username = name
    
    # a getter method, extracts email from object
    @property
    def userstory(self):
        return self._userstory
    
    # a setter function, allows name to be updated after initial object creation
    @userstory.setter
    def userstory(self, score):
        self._userstory = score

    # a getter method, extracts email from object
    @property
    def aistory(self):
        return self._aistory
    
    # a setter function, allows name to be updated after initial object creation
    @aistory.setter
    def aistory(self, score):
        self._aistory = score
    
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
            "username": self.name,
            "user-story": self.userstory,
            "AI-story": self.aistory,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", score=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(score) > 0:
            self.userstory = score
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
def initFables():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""