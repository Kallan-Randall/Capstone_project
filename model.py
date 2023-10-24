"""Models for recipe app."""
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    recipes = db.relationship('Recipe', backref='user')


    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"

class Recipe(db.Model):
    """A recipe"""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.Integer)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cooking_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = relationship("User", backref="recipes")

    def __repr__(self):
        return f"<Recipe recipe_id={self.recipe_id}>" 



def connect_to_db(flask_app, db_uri=os.environ["DATABASE_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
 
    connect_to_db(app)
    print("Connected to the db!")