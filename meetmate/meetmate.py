from random import randint
from flask import Flask, render_template, redirect, url_for, session, request, g

import Database
import Meet
import Setting
import User
import Group
import os
import SmsProvider
import MailProvider

Setting.setting_init()
setting = Setting.setting

Database.database_init(
    setting["db_name"],
    setting["db_host"],
    setting["db_port"],
    setting["db_user"],
    setting["db_pass"],
)

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/test")
def test():
    group = Group.Group.get_by_name("Testowa")
    user = User.User("608491b5dc5221509036541d")
    user.del_group(group)
    users = group.get_all_users()
    return str(len(users))

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"]) #TODO: Do this by AJAX api calls
def login():
    if "user" in session:
        user = User.User(session["user"])
        if user.type == User.UserType.ADMINISTRATOR:
            return redirect(url_for("admin_panel"))
        elif user.type == User.UserType.ORGANIZER:
            return redirect(url_for("organizer_panel"))
        else:
            return redirect(url_for("user_panel"))

    if request.method == "POST":
        try:
            user = User.User.auth(request.form["email"], request.form["password"])
        except:
            return redirect(url_for("index")) # invalid post data, email or password

        token = str(randint(0,999999)).zfill(6)
        SmsProvider.send_2fa(user.phone_number, token)
        session["auth_id"] = str(user.id)
        session["auth_token"] = token
        return redirect(url_for("auth"))

    return render_template("login.html")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if "user" in session:
        user = User.User(session["user"])
        if user.type == User.UserType.ADMINISTRATOR:
            return redirect(url_for("admin_panel"))
        elif user.type == User.UserType.ORGANIZER:
            return redirect(url_for("organizer_panel"))
        else:
            return redirect(url_for("user_panel"))

    if request.method == "POST":
        if request.form["password"] == session["auth_token"]:
            user = User.User(session["auth_id"])
            session["user"] = str(user.id)
            session.pop("auth_id", None)
            session.pop("auth_token", None)
            if user.type == User.UserType.ADMINISTRATOR:
                return redirect(url_for("admin_panel"))
            elif user.type == User.UserType.ORGANIZER:
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

@app.route("/organizer")
def organizer_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("login"))

    return render_template("organizer.html")

@app.context_processor
def organizer_panel():
    if "user" in session:
        user = User.User(session["user"])
        meetings = Meet.Meet.get_by_organizer(user)
        return dict(meetings=meetings)
    return dict(meetings=[])


@app.route("/admin")
def admin_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ADMINISTRATOR:
        return redirect(url_for("login"))

    return render_template("admin.html")


@app.context_processor
def admin_panel():
    users = User.User.get_all_users()
    return dict(users=users)


@app.route("/user")
def user_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    return render_template("user.html")


@app.route("/meetings_history")
def meetings_history():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    return render_template("user_history.html")

@app.context_processor
def meetings_history():
    if "user" in session:
        user = User.User(session["user"])
        meetings = Meet.Meet.get_by_user(user)
        return dict(meetings=meetings)
    return dict(meetings=[])


@app.route("/meet/<meet_id>")
def meet_panel(meet_id):
    return str(meet_id)


@app.route("/test_register")
def test_register():
    try:
        User.User.add_user("admin@admin.com", "123456", "000000000", "Adam", "Małysz")
    except User.ExistError:
        return("User already exist")

    return redirect(url_for("index"))




