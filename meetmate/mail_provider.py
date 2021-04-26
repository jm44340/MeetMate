import setting
import smtplib

setting.setting_init()
setting = setting.setting


def send_mail(receiver, message):
	with smtplib.SMTP(setting["mail_host"], setting["mail_port"]) as server:
		server.login(setting["mail_user"], setting["mail_pass"])
		server.sendmail(setting["mail_sender"], receiver, message)
