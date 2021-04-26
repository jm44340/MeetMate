import setting
import requests

setting.setting_init()
setting = setting.setting


def send_sms(recipient, message):
	url = setting["sms_url"]
	data = {
		"login": setting["sms_user"],
		"pass": setting["sms_pass"],
		"msg_type": setting["sms_type"],
		"recipient": recipient,
		"message": message,
		"sandbox": "1"  # TODO set to 0 to disable sandbox
	}
	requests.post(url=url, data=data)
