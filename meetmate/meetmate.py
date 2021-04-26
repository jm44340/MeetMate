from random import randint
from flask import Flask, render_template, redirect, url_for, session, request, g
from user import User, UserType

import database
import setting
import user
import os
import sms_provider
import mail_provider

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
        user = User(session["user"])
        if user.type == UserType.ADMINISTRATOR:
            return redirect(url_for("admin_panel"))
        elif user.type == UserType.ORGANIZER:
            return redirect(url_for("organizer_panel"))
        else:
            return redirect(url_for("user_panel"))

    if request.method == "POST":
        try:
            user = User.auth(request.form["email"], request.form["password"])
        except:
            return redirect(url_for("index")) # invalid post data, email or password

        token = str(randint(0,999999)).zfill(6)
        sms_provider.send_2fa(user.phone_number, token)
        session["auth_id"] = str(user.id)
        session["auth_token"] = token
        return redirect(url_for("auth"))

    return render_template("login.html")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if "user" in session:
        user = User(session["user"])
        if user.type == UserType.ADMINISTRATOR:
            return redirect(url_for("admin_panel"))
        elif user.type == UserType.ORGANIZER:
            return redirect(url_for("organizer_panel"))
        else:
            return redirect(url_for("user_panel"))

    if request.method == "POST":
        if request.form["password"] == session["auth_token"]:
            user = User(session["auth_id"])
            session["user"] = str(user.id)
            session.pop("auth_id", None)
            session.pop("auth_token", None)
            if user.type == UserType.ADMINISTRATOR:
                return redirect(url_for("admin_panel"))
            elif user.type == UserType.ORGANIZER:
                return redirect(url_for("organizer_panel"))
            else:
                return redirect(url_for("user_panel"))
        else:
            return redirect(url_for("index"))
    if "auth_token" in session:
        return render_template("authentication.html")
    else:
        return redirect(url_for("login"))





@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


#@app.route("/reset") #TODO
#def reset_password(): #TODO
    #return redirect(url_for("index")) #TODO


@app.route("/admin")
def admin_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User(session["user"])
    if user.type != UserType.ADMINISTRATOR:
        return redirect(url_for("login"))

    return render_template("admin.html")


@app.route("/user")
def user_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User(session["user"])
    if user.type != UserType.USER:
        return redirect(url_for("login"))

    return render_template("user.html")


@app.route("/meet/<meet_id>")
def meet_panel(meet_id):
    return str(meet_id)


@app.route("/test_register")
def test_register():
    try:
        User.add_user("admin@admin.com", "123456", "000000000", "Adam", "Małysz")
    except user.ExistError:
        return("User already exist")

    return redirect(url_for("index"))




