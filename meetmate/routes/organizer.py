from flask import render_template, redirect, url_for, session

from Setting import setting
from meetmate import app
import Meet
import User


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
