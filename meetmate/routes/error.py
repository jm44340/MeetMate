import uuid
from flask import render_template, redirect, url_for
from meetmate import app


@app.route("/error/<error_type>")
def error(error_type):
	id = str(uuid.uuid4())
	# HTTP ERRORS
	if error_type == "404":
		return render_template("error.html", code="404", description="nie znaleziono", id=id), 404
	elif error_type == "500":
		return render_template("error.html", code="500", description="błąd serwera", id=id), 500

	# MEETINGS ERRORS
	elif error_type == "meet-not-active":
		return render_template("error.html", code="403", description="spotkanie jest nieaktywne", id=id), 403
	elif error_type == "meet-not-exist":
		return render_template("error.html", code="404", description="spotkanie nie istnieje", id=id), 404

	# QR ERRORS
	elif error_type == "qr-not-valid":
		return render_template("error.html", code="400", description="nieprawidłowy kod qr", id=id), 400

	# DEFAULT ERROR
	return render_template("error.html", code="501", description="błąd", id=id), 501


@app.errorhandler(404)
def errorhandler_404(error_type):
	return error("404")


@app.errorhandler(500)
def errorhandler_500(error_type):
	return error("500")
