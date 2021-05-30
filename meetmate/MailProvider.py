import Setting
import smtplib

def send_mail(receiver, message):
	with smtplib.SMTP(Setting.setting["mail_host"], Setting.setting["mail_port"]) as server:
		server.login(Setting.setting["mail_user"], Setting.setting["mail_pass"])
		server.sendmail(Setting.setting["mail_sender"], receiver, message)
