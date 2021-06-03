from flask import Flask, redirect, url_for
import Database
import Setting
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
from routes import admin, authorization, error, organizer, test, user

@app.route("/")
def index():
    return redirect(url_for("login"))
