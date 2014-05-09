#my_db.py
#module for interfacing with GAE datastore

import datetime
from google.appengine.ext import db
from google.appengine.api import users
import webapp2
from google.appengine.ext.db import Key
from webapp2_extras import security
import random

#Customer Record
class User(db.Model):
    name = db.StringProperty()
    password = db.StringProperty()
    txn_id = db.StringProperty()
    login_attempts = db.IntegerProperty()
    password_resets = db.IntegerProperty()
    previous_passwords = db.StringListProperty()
    email = db.StringProperty()

#Password reset Token
class PasswordReset(db.Model):
    email = db.StringProperty()
    time = db.DateTimeProperty(auto_now=True) #simply records last time PasswordReset was stored in db

    def __str__(self):
        return self.email

#Create new user
def new_user(name, email, txn_id='123'):
    return User(name=name, email=email, key_name=email, login_attempts=0, password_resets=0, previous_passwords=[], txn_id=txn_id)

#Get user from database
def get(email):
    return db.get(Key.from_path('User', email))

#Generate new password reset token
def new_reset(email):
    return PasswordReset(email=email, key_name=str(random.uniform(0, 1)))
