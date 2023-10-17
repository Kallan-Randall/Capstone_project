"""This module is responsable for CRUD operations in the Postgres database."""
from sqlalchemy import or_
from model import db, connect_to_db, User, Recipe

#Functions below

def create_user(email, username, password):
    """Creates a new user object and returns it."""
    new_user = User(email=email, username=username, password=password)
    return new_user

def get_user_by_email(email):
    """Gets a user from database by email and returns it."""
    return User.query.filter(User.email == email).first()

def get_user_by_username_or_email(identifier):
    """Gets a user from the database by username or email and returns it."""
    return User.query.filter(or_(User.username == identifier, User.email == identifier)).first()







