import MailProvider
import Meet
import SmsProvider
import User
from flask import render_template, redirect, url_for, session
from meetmate import app
from routes import error


@app.route("/test/add_user/<email>/<password>/<phone_number>/<first_name>/<last_name>")
def test_add_user(email, password, phone_number, first_name, last_name):
	try:
		User.User.add_user(email, password, phone_number, first_name, last_name)
	except User.ExistError:
		return error.error("user-already-exist")
	return "user added"


@app.route("/test/create_meet/<name>/<localization>/<description>")
def test_create_meet(name, localization, description):
	if "user" in session:
		user = User.User(session["user"])
		if user.type == User.UserType.ORGANIZER:
			meet = Meet.Meet.create_meet(name, user, localization, description)
	return "meeting created"


@app.route("/test/mail/<receiver>/<subject>/<message>")
def test_mail(receiver, subject, message):
	MailProvider.send_mail(receiver, subject, message)
	return "mail send"


@app.route("/test/sms/<receiver>/<message>")
def test_sms(receiver, message):
	SmsProvider.send_sms(receiver, message)
	return "sms send"
