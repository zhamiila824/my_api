import os
import sys

from flask import Flask, render_template, g, session
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
# engine = create_engine('postgresql://scott:tiger@localhost/')
# with Session(engine) as db_session:
#     session.add(some_object)
#     session.add(some_other_object)
#     session.commit()

########################
# Configure Secret Key #
########################
def install_secret_key(app, filename="secret_key"):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config["SECRET_KEY"] = open(filename, "rb").read()
    except IOError:
        print("Error: No secret key. Create it with:")
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print("mkdir -p {filename}".format(filename=full_path))
        print("head -c 24 /dev/urandom > {filename}".format(filename=filename))
        sys.exit(1)


if not app.config["DEBUG"]:
    install_secret_key(app)


from app.users.models import User
from app.users.views import users as usersModule
from app.products.views import products as productsModule


@app.before_request
def before_request():
    """
    pull user's profile from database before every request
    """
    g.user = None
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.route("/")
def home():
    return render_template("index.html")


app.register_blueprint(usersModule)
app.register_blueprint(productsModule)
