from flask import Flask, render_template, redirect, url_for, session

import Database
import Meet
import Setting
import User
import Group
import Presence
import os

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
from routes import error, test, authorization


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


# @app.route("/reset") #TODO
# def reset_password(): #TODO
# return redirect(url_for("index")) #TODO

@app.route("/organizer")
def organizer_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("login"))
    logged_user = user.first_name+' '+user.last_name
    return render_template("organizer.html", logged_user=logged_user)


@app.route("/organizer_meetings")
def organizer_meetings():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("login"))
    meetings = Meet.Meet.get_by_organizer(user)
    return render_template("organizer_meetings.html", meetings=meetings)


@app.route("/admin")
def admin_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ADMINISTRATOR:
        return redirect(url_for("login"))

    logged_user = user.first_name + ' ' + user.last_name
    users = User.User.get_all_users()
    return render_template("admin.html", users=users, logged_user=logged_user)

@app.route("/user")
def user_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    logged_user = user.first_name+' '+user.last_name
    return render_template("user.html", logged_user=logged_user)



@app.route("/new_group")
def new_group():
    return render_template("new_group.html")


@app.route("/meetings_history")
def meetings_history():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    meetings = Meet.Meet.get_by_user(user)
    return render_template("user_history.html", meetings=meetings)


@app.route("/new_meeting")
def new_meeting():
    return render_template("new_meeting.html")


@app.route("/meet/<meet_id>")
def meet_qr(meet_id):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("login"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return redirect("https://http.cat/404")

    qr_data = meet.get_qr_data()
    return render_template("qr.html", qr_data=qr_data, qr_time=setting["qr_time"])


@app.route("/meet/<meet_id>/<qr_hash>")
def meet_qr_check(meet_id, qr_hash):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return error.error("meet-not-exist")

    if meet.status != Meet.MeetStatus.ACTIVE:
        return error.error("meet-not-active")

    if not meet.check_qr_data(qr_hash):
        return error.error("qr-not-valid")

    presence = Presence.Presence.new_presence(meet, user)
    return "OK"


@app.route("/scan_qr")
def scan_qr():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))
    return render_template("scan_qr.html")



