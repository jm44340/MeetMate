from flask import Flask, render_template, redirect, url_for, session, request, g
from user import User, UserType

import database
import setting
import user
import os

setting.setting_init()
setting = setting.setting

database.database_init(
    setting["db_name"],
    setting["db_host"],
    setting["db_port"],
    setting["db_user"],
    setting["db_pass"],
)

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"]) #TODO: Do this by AJAX api calls
def login():
    if "user" in session:
        redirect(url_for("test")) # redirect to user panel

    if request.method == "POST":
        try:
            user = User.auth(request.form["email"], request.form["password"])
        except:
            return redirect(url_for("index")) # invalid post data, email or password

        session["user"] = str(user.id)
        return redirect(url_for("test"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/admin")
def admin():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User(session["user"])
    if user.type != UserType.ADMINISTRATOR:
        return redirect(url_for("login"))

    return render_template("admin.html")

@app.route("/meet/<meet_id>")
def meet(meet_id):
    return str(meet_id)

@app.route("/test")
def test():
    if "user" in session.keys():
        user = User(session["user"])
        return "You are logon! - " + user.first_name + " " + user.last_name
    else:
        return "Please login first"

@app.route("/test_register")
def test_register():
    try:
        User.add_user("test@test.com", "123456", "000000000", "Adam", "Małysz")
    except user.ExistError:
        return("User already exist")

    return redirect(url_for("index"))