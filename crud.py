"""This module is responsible for CRUD operations in the Postgres database."""
from sqlalchemy import or_
from model import db, connect_to_db, User, Recipe

#Functions 

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

def get_recipes(user:User):
    """Gets all recipes by user id."""
    return Recipe.query.filter_by(user_id=user.user_id).all()

def get_5_last_recipes():
    """Gets 5 last recipes created"""
    return Recipe.query.order_by(Recipe.recipe_id.desc()).limit(5).all()

def create_recipe(title, category, description, ingredients, instructions, cooking_time, user):
    """Creates a new recipe object and returns it."""
    new_recipe = Recipe(title=title, category=category, description=description, ingredients=ingredients, instructions=instructions, cooking_time=cooking_time, user=user)
    return new_recipe

def get_recipe_by_id(recipe_id):
    """Gets a recipe by recipe_id"""
    return Recipe.query.get(recipe_id)

def update_recipe(recipe, title, category, description, ingredients, instructions, cooking_time):
    """Updates existing recipe with new information"""
    recipe.title = title
    recipe.category = category
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.instructions = instructions
    recipe.cooking_time = cooking_time
    db.session.commit()

def delete_recipe(recipe):
    """Deletes a recipe from the database"""
    db.session.delete(recipe)
    db.session.commit()