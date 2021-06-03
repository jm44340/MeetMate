import Meet
import User
from flask import render_template, redirect, url_for, session
from meetmate import app
from routes import error


@app.route("/test/add_user/<email>/<password>/<phone_number>/<first_name>/<last_name>")
def add_user(email, password, phone_number, first_name, last_name):
	try:
		User.User.add_user(email, password, phone_number, first_name, last_name)
	except User.ExistError:
		return error.error("user-already-exist")
	return redirect(url_for("index"))


@app.route("/test/create_meet/<name>/<localization>/<description>")
def create_meet(name, localization, description):
	if "user" in session:
		user = User.User(session["user"])
		if user.type == User.UserType.ORGANIZER:
			meet = Meet.Meet.create_meet(name, user, localization, description)
	return redirect(url_for("index"))
