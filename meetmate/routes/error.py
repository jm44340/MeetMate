import uuid
from flask import render_template, session

import Log
import User
from meetmate import app

@app.route("/error/<error_type>")
def error(error_type):
	error_id = str(uuid.uuid4())
	user_id = None
	if "user" in session:
		user_id = User.User(session["user"]).id


	# AUTHORIZATION ERRORS
	if error_type == "user-already-exist":
		return render_template("error.html", code="409", description="użytkownik już istnieje", id=error_id), 409

	# HTTP ERRORS
	elif error_type == "404":
		return render_template("error.html", code="404", description="nie znaleziono", id=error_id), 404
	elif error_type == "500":
		return render_template("error.html", code="500", description="błąd serwera", id=error_id), 500

	# MEETINGS ERRORS
	elif error_type == "meet-not-active":
		return render_template("error.html", code="403", description="spotkanie jest nieaktywne", id=error_id), 403
	elif error_type == "meet-not-exist":
		return render_template("error.html", code="404", description="spotkanie nie istnieje", id=error_id), 404

	# QR ERRORS
	elif error_type == "qr-not-valid":
		return render_template("error.html", code="400", description="nieprawidłowy kod qr", id=error_id), 400

	# CSV FILE ERRORS
	elif error_type == "empty-file":
		Log.Log.add_entry(user_id,"POST","import użytkowników","406","plik nie został przesłany")
		return render_template("error.html", code="406", description="plik nie został przesłany", id=error_id), 406
	elif error_type == "not-csv-file":
		Log.Log.add_entry(user_id, "POST", "import użytkowników", "406", "plik musi posiadać rozszerzenie csv")
		return render_template("error.html", code="406", description="plik musi posiadać rozszerzenie csv", id=error_id), 406

	# DEFAULT ERROR
	return render_template("error.html", code="501", description="błąd", id=error_id), 501


@app.errorhandler(404)
def errorhandler_404(error_type):
	return error("404")


@app.errorhandler(500)
def errorhandler_500(error_type):
	return error("500")
