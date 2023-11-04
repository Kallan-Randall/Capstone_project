"""Server for recipe app."""

# imports here
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from model import connect_to_db, db, Recipe, User
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "this is secret key"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    last_5_recipes = crud.get_5_last_recipes()
    
    # creator_usernames = [(recipe.creator.username) if recipe.creator else 'Unknown' for recipe in last_5_recipes]
    
    # return render_template("home.html", last_5_recipes=last_5_recipes, creator_usernames=creator_usernames)
    return render_template("home.html", last_5_recipes=last_5_recipes)

@app.route("/register")
def register_page():
    return render_template("register.html")

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

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    identifier = request.form['email_or_username']
    password = request.form['password']

    user = crud.get_user_by_username_or_email(identifier)

    if user and user.password == password:
        login_user(user)
        flash(f"Welcome back {user.username}")
        
        session['username'] = user.username

        return redirect("/")
        
    else:
        flash("login failed. Check you email/username and password.")
        return redirect("/")
    
@app.route("/user")
@login_required
def user():
    
    user_recipes = crud.get_recipes(current_user)
    
    return render_template("/user.html", user_recipes=user_recipes)

@app.route("/recipes")
@login_required
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

    new_recipe = crud.create_recipe(title, category, description, ingredients, instructions, cooking_time, current_user)

    db.session.add(new_recipe)
    db.session.commit()

    flash("Recipe created successfully!")

    return redirect("/recipes")

@app.route("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id) 
    if recipe:
        return render_template("recipe_details.html", recipe=recipe)
    else:
        flash("Recipe not found.")
        return redirect("/")

@app.route("/update_recipe/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def update_recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    if not recipe:
        flash("Recipe not found.")
        return redirect("/user")
    
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        instructions  = request.form.get("instructions")
        cooking_time = request.form.get("cooking_time")

        recipe.title = title
        recipe.category = category
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cooking_time = cooking_time

        db.session.commit()
        flash("Recipe updated!")
        return redirect("/user")
    
    return render_template("update_recipe.html", recipe=recipe)

@app.route("/search", methods=["GET"])
def search_recipes():
    query = request.args.get("q")

    search_results = crud.search_recipes(query)

    return render_template("search_results.html", search_results=search_results)

@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    recipe = crud.get_recipe_by_id(recipe_id)
    if not recipe:
        flash("Recipe not found.")
        return redirect("/user")
    
    if recipe.user_id != current_user.user_id:
        flash("You can only delete your own recipe.")
        return redirect ("/user")
    
    db.session.delete(recipe)
    db.session.commit()

    flash("Recipe deleted!")
    return redirect("/user")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.")
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)