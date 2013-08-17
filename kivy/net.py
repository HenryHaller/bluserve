import json, urllib
HOST="raspberrypi"
PORT=8080

def get_database_from_server():
	url = "http://%s:%d/get_json" % (HOST, PORT)
	return json.loads(urllib.urlopen(url).read())


def get_alias_for_address(address):
	url = "http://%s:%d/get_json" % (HOST, PORT)
	data = {"device_address":address}
	encoded_data = urllib.urlencode(data)
	alias = urllib.urlopen("http://%s:%d/get_alias_for_address" % (HOST, PORT), encoded_data)
	return alias.read()

def set_state(device_address):
	data = {"device_address": device_address}
	encoded_data = urllib.urlencode(data)
	urllib.urlopen("http://%s:%d/set_state" % (HOST, PORT), encoded_data)
