from flask import Flask, render_template, redirect, url_for, session, g
from database import Database
import setting
import os

setting.setting_init()
setting = setting.setting

db = Database(
    setting["db_name"],
    setting["db_host"],
    setting["db_port"],
    setting["db_user"],
    setting["db_pass"],
)
app = Flask(__name__)
app.secret_key = os.urandom(16)

#https://flask.palletsprojects.com/en/master/templating/
#https://jinja.palletsprojects.com/en/2.11.x/templates/
#https://flask.palletsprojects.com/en/master/quickstart/#sessions

@app.context_processor
def inject_title():
    return dict(title="MeetMate")

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    g.subtitle = "Login page"
    user = "not logged in"

    if "username" in session:
        user = session["username"]

    return render_template("login.html", user=user)

@app.route("/login_test")
def login_test():
    session["username"] = "Test"
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    return redirect(url_for("admin"))

@app.route("/meet/<meet_id>")
def meet(meet_id):
    return str(meet_id)