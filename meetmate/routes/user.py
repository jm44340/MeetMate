from flask import render_template, redirect, url_for, session
from meetmate import app
from routes import error
import Meet
import Presence
import User


@app.route("/user")
def user_panel():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    logged_user = user.first_name+' '+user.last_name
    return render_template("user.html", logged_user=logged_user)



@app.route("/meetings_history")
def meetings_history():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))

    meetings = Meet.Meet.get_by_user(user)
    return render_template("user_history.html", meetings=meetings)


@app.route("/scan_qr")
def scan_qr():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("login"))
    return render_template("scan_qr.html")


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
