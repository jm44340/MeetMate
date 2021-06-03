import Setting
import smtplib


def send_mail(receiver, subject, message):
	request = "From: " + Setting.setting["mail_sender"] + "\nTo: " + receiver + "\nSubject: " + subject + "\n" + message
	with smtplib.SMTP(Setting.setting["mail_host"], Setting.setting["mail_port"]) as server:
		server.login(Setting.setting["mail_user"], Setting.setting["mail_pass"])
		server.sendmail(Setting.setting["mail_user"], receiver, request.encode('utf-8'))
