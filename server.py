"""Server for recipe app."""

# imports here
from flask import Flask, render_template, request, flash, session, redirect, url_for

from model import connect_to_db, db, Recipe, User
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "this is secret key"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    last_5_recipes = crud.get_5_last_recipes()
    
    creator_usernames = [(recipe.creator.username) if recipe.creator else 'Unknown' for recipe in last_5_recipes]
    
    return render_template("home.html", last_5_recipes=last_5_recipes, creator_usernames=creator_usernames)

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/recipes")
def recipe():
    return render_template("recipes.html")

@app.route("/recipes", methods=["POST"])
def create_recipe():
    """Creates a new recipe"""
    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")
    ingredients = request.form.get("ingredients")
    instructions = request.form.get("instructions")
    cooking_time = request.form.get("cooking_time")

    new_recipe = crud.create_recipe(title, category, description, ingredients, instructions, cooking_time)

    db.session.add(new_recipe)
    db.session.commit()

    flash("Recipe created successfully!")

    return redirect("/recipes")

@app.route("/users", methods=["POST"])
def register_user():
    "Creates a new user."
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Email has already been used. Try a different email.")
    else:
        user = crud.create_user(email, username, password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created! Welcome {user.username}")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    identifier = request.form['email_or_username']
    password = request.form['password']

    user = crud.get_user_by_username_or_email(identifier)

    if user and user.password == password:
        flash(f"Welcome back {user.username}")
        return redirect("/")
    else:
        flash("login failed. Check you email/username and password.")
        return redirect("/")
    



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)