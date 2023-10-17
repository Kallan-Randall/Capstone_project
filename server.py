"""Server for recipe app."""

# imports here
from flask import Flask, render_template, request, flash, session, redirect, url_for

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "this is secret key"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    return render_template("home.html")

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