from flask import render_template, redirect, url_for, session
from meetmate import app
import User


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


@app.route("/new_group")
def new_group():
    return render_template("new_group.html")
