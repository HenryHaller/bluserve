#!/usr/bin/python
STATE_LOCATION = "/var/tmp/bluserve/"


import os, anydbm, json
os.system("mkdir -p " + STATE_LOCATION)
def get_state_database1():
    try:
        return anydbm.open(STATE_LOCATION + "state2", 'c')
    except:
        print "failed to get state db..."

#class state_database:
#	def __init__(self, state_dict):
#		self.state_dict = state_dict
#	def sync(self):
#		json.dump(self.state_dict, open(STATE_LOCATION + "state2", 'w'))
#	def __getitem__(self, item):
#		return self.state_dict.__getitem__(item)
#	def __iter__(self):
#		return self.state_dict.__iter__()


class state_database(dict):
	def __init__(self, state_dict):
		for a in state_dict: self[a] = state_dict[a]
	def sync(self):
		json.dump(self, open(STATE_LOCATION + "state2", 'w'))

def get_state_database():
#	try:
	state_dict = json.load(open(STATE_LOCATION + "state2", 'r'))
	return state_database(state_dict)
#	except:
#		print "failed to get state db..."


