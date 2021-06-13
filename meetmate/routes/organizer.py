from flask import render_template, redirect, url_for, session, request
import json

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
        return redirect(url_for("index"))
    logged_user = user.first_name+' '+user.last_name
    return render_template("organizer.html", logged_user=logged_user)


@app.route("/organizer_meetings")
def organizer_meetings():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("index"))
    meetings = Meet.Meet.get_by_organizer(user)
    return render_template("organizer_meetings.html", meetings=meetings)


@app.route("/new_meeting")
def new_meeting():
    return render_template("new_meeting.html")

@app.route("/edit_meeting/<meet_id>", methods=['POST'])
def edit_meeting(meet_id):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("index"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return redirect("https://http.cat/404")

    try:
        action = request.form.get('action')
        if action == "get":
            return json.dumps(
                {
                    "status": "OK",
                    "data": {
                        meet.name,
                        meet.description,
                        meet.start_time,
                        meet.stop_time,
                        meet.localization,
                        meet.status.value,
                        meet.longitude,
                        meet.latitude,
                        meet.radius,
                        meet.link_id
                    }
                }
            )

        elif action == "edit":
            name = request.form.get("name")
            description = request.form.get("description")
            start_time = request.form.get("start_time")
            stop_time = request.form.get("stop_time")
            localization = request.form.get("localization")
            status = request.form.get("status")
            longitude = request.form.get("longitude")
            latitude = request.form.get("latitude")
            radius = request.form.get("radius")

            meet.name = name
            meet.description = description
            meet.start_time = start_time
            meet.stop_time = stop_time
            meet.localization = localization
            meet.status = Meet.MeetStatus(status)
            meet.longitude = longitude
            meet.latitude = latitude
            meet.radius = radius

            return json.dumps({"status": "OK"})
    except Exception as e:
        print(e)
        return json.dumps({"status": "ERROR"})

@app.route("/meet/<meet_id>")
def meet_qr(meet_id):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("index"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return redirect("https://http.cat/404")

    qr_data = meet.get_qr_data()
    return render_template("qr.html", qr_data=qr_data, qr_time=setting["qr_time"])

@app.route("/raport/<meet_id>")
def raport(meet_id):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.ORGANIZER:
        return redirect(url_for("index"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return redirect("https://http.cat/404")

    # TODO

