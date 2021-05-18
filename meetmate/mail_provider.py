import setting
import smtplib

def send_mail(receiver, message):
	with smtplib.SMTP(setting.setting["mail_host"], setting.setting["mail_port"]) as server:
		server.login(setting.setting["mail_user"], setting.setting["mail_pass"])
		server.sendmail(setting.setting["mail_sender"], receiver, message)
