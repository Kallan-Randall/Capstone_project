"""Server for recipe app."""

# imports here
from flask import Flask, render_template, request, flash, session, redirect, url_for

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "this is secret key"
app.jinja_env.undefined = StrictUndefined


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)