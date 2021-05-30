
import json

setting = None

def setting_init():
    try:
        with open('setting.json') as json_file:
            global setting
            setting = json.load(json_file)
    except:
        print("Error open setting.json")
        exit(1)