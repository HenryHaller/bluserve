import json, urllib
HOST="192.168.2.25"
PORT=8080

def get_database_from_server():
	url = "http://%s:%d/get_json" % (HOST, PORT)
	return json.loads(urllib.urlopen(url).read())


def set_state(device_address):
	data = {"device_address": device_address}
	encoded_data = urllib.urlencode(data)
	urllib.urlopen("http://%s:%d/set_state" % (HOST, PORT), encoded_data)
