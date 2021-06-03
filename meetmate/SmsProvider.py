import Setting
import requests


def send_sms(recipient, message):
	url = Setting.setting["sms_host"]
	data = {
		"login": Setting.setting["sms_user"],
		"pass": Setting.setting["sms_pass"],
		"msg_type": Setting.setting["sms_type"],
		"recipient": recipient,
		"message": message,
		"sandbox": "0"
	}
	requests.post(url=url, data=data)


def send_2fa(recipient, code):
	message = "MeetMate: Twoje jednorazowe haslo SMS do autoryzacji to " + code
	# send_sms(recipient, message) #TODO ENABLE SMS SENDING
	print(message)
