import base64
import os
import uuid
import csv
from flask import render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename

import MailProvider
from Log import Log
from meetmate import app
import User
from routes.error import error


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


@app.route("/logs")
def logs():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ADMINISTRATOR:
        return redirect(url_for("login"))
    entries = Log.get_logs()
    Log.add_entry(user.id, "GET", "logi systemowe", "200", "ładowanie powiodło się")
    return render_template("logs.html", entries=entries)


@app.route("/new_group")
def new_group():
    return render_template("new_group.html")


@app.route("/import_users", methods=['GET', 'POST'])
def import_users():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ADMINISTRATOR:
        return redirect(url_for("login"))
    if request.method == 'GET':
        return render_template("import_users.html")
    if request.method == 'POST':
        ret = redirect(url_for("index"))
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(filename)
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                password = base64.b64encode(os.urandom(8)).decode()
                try:
                    User.User.add_user(row['email'], password, row['phone_number'], row['first_name'], row['last_name'])
                    msg = "Witaj " + row['first_name'] + ' ' + row['last_name'] + ",\nTwoje haslo pierwszego logowania to: " + password + "\n"
                    MailProvider.send_mail(row['email'], "Haslo - pierwsze logowanie", msg)
                except:
                    ret = error("user-already-exist")
        os.remove(filename)
        return ret


@app.route("/add_user", methods=['POST'])
def add_user():
    if "user" not in session.keys():
        return redirect(url_for("login"))
    user = User.User(session["user"])
    if user.type != User.UserType.ADMINISTRATOR:
        return redirect(url_for("login"))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        phone_number = request.form.get('phone')
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        try:
            User.User.add_user(email, password, phone_number, first_name, last_name)
        except:
            return error("user-already-exist")

    return redirect(url_for("index"))
