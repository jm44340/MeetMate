from random import randint
from flask import render_template, redirect, url_for, session, request
from meetmate import app
import SmsProvider
import User


def __redirect_to_panel():
    user = User.User(session["user"])
    if user.type == User.UserType.ADMINISTRATOR:
        return redirect(url_for("admin_panel"))
    elif user.type == User.UserType.ORGANIZER:
        return redirect(url_for("organizer_panel"))
    else:
        return redirect(url_for("user_panel"))


@app.route("/login", methods=["GET", "POST"])  # TODO: Do this by AJAX api calls
def login():
    if "user" in session:
        return __redirect_to_panel()

    if request.method == "POST":
        try:
            user = User.User.auth(request.form["email"], request.form["password"])
        except:
            return redirect(url_for("index"))  # invalid post data, email or password

        token = str(randint(0, 999999)).zfill(6)
        SmsProvider.send_2fa(user.phone_number, token)
        session["auth_id"] = str(user.id)
        session["auth_token"] = token
        return redirect(url_for("auth"))

    return render_template("login.html")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if "user" in session:
        return __redirect_to_panel()

    if request.method == "POST":
        # TODO disable 2fa backdoor
        if request.form["password"] == session["auth_token"] or request.form["password"] == "0":
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


#TODO password reset
@app.route("/reset")
def reset_password():
    return redirect(url_for("index"))
