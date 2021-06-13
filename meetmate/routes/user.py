import base64
import os
import json

from flask import render_template, redirect, url_for, session, request
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
        return redirect(url_for("index"))

    logged_user = user.first_name+' '+user.last_name
    return render_template("user.html", logged_user=logged_user)



@app.route("/meetings_history")
def meetings_history():
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("index"))

    meetings = Meet.Meet.get_by_user(user)
    return render_template("user_history.html", meetings=meetings)


@app.route("/scan_qr")
def scan_qr():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("index"))
    return render_template("scan_qr.html")

@app.route("/meet/<meet_id>/<qr_hash>", methods=['GET', 'POST'])
def meet_qr_check(meet_id, qr_hash):
    if "user" not in session.keys():
        return redirect(url_for("login"))

    user = User.User(session["user"])
    if user.type != User.UserType.USER:
        return redirect(url_for("index"))

    try:
        meet = Meet.Meet.get_by_linkid(meet_id)
    except Meet.ExistError:
        return error.error("meet-not-exist")

    if meet.status != Meet.MeetStatus.ACTIVE:
        return error.error("meet-not-active")

    if not meet.check_qr_data(qr_hash):
         return error.error("qr-not-valid")

    if request.method == 'POST':
        try:
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
        except:
            return json.dumps({"status": "ERROR"})

        if not meet.check_localization(float(longitude), float(latitude)):
            return json.dumps({"status": "TOO FAR"})

        Presence.Presence.new_presence(meet, user)
        return json.dumps({"status": "OK"})

    return render_template("confirm.html")

# @app.route("/confirm", methods=['GET', 'POST'])
# def meet_qr_confirm():
#     user = User.User(session["user"])
#     if user.type != User.UserType.USER:
#         return redirect(url_for("login"))
#     if request.method == 'GET':
#         if "meet_id" not in session.keys():
#             return redirect(url_for("index"))
#         meet_id = session["meet_id"]
#         return render_template("confirm.html", meet=meet_id)

#     if request.method == 'POST':
#         latitude = request.form.get('latitude')
#         longitude = request.form.get('longitude')
#         meet_id = session["meet_id"]
#         session.pop("meet_id", None)
#         meet = Meet.Meet.get_by_linkid(meet_id)
#         if not meet.check_localization(float(longitude), float(latitude)):
#             return "ERR"
#         presence = Presence.Presence.new_presence(meet, user)
#         return "OK"

#     return redirect(url_for('index'))