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
class Fable(db.Model):
    __tablename__ = 'fables'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=False, nullable=False)
    _userbody = db.Column(db.String(255), unique=True, nullable=False)
    _aibody = db.Column(db.String(255), unique=True, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, username, userbody, aibody):
        self._username = username    # variables with self prefix become part of the object, 
        self._userbody = userbody
        self._aibody = aibody

    # a name getter method, extracts name from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows name to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username
    
    # a getter method, extracts email from object
    @property
    def userbody(self):
        return self._userbody
    
    # a setter function, allows name to be updated after initial object creation
    @userbody.setter
    def userbody(self, userbody):
        self._userbody = userbody

    # a name getter method, extracts name from object
    @property
    def aibody(self):
        return self._aibody
    
    # a setter function, allows name to be updated after initial object creation
    @aibody.setter
    def aibody(self, aibody):
        self._aibody = aibody
        
    # check if uid parameter matches user id in object, return boolean
    def is_userbody(self, userbody):
        return self._userbody == userbody
    
    
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
            "userbody": self.userbody,
            "aibody": self.aibody
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, username="", userbody=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(userbody) > 0:
            self.userbody = userbody
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
    u1 = Fable(username='raisinbran25', userbody='Hello Peter... welcome to fortnite', aibody='BHIAEFN')
    fables = [u1]
    for fable in fables:
        fable.create()
            
