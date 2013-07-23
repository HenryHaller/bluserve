#!/usr/bin/python
from Tkinter import *
from bluserve_library import authorize_device, standby_device, get_alias
import state
import time
import threading
import Tkinter
import threading
class bluserve_tk(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
	self.daemon = True
        self.start()
    def generateAddressFunction(self, address=None, action=None):
	if action == "authorize":
		def addressFunction():
			db = state.get_state_database()
			for a in db:
				standby_device(a)
				db[a] = 'standby'
			authorize_device(address)
			db[address] = action
			db.sync()
			self.refreshWidgets()
			print "got address", address, "to authorize"
	if action == "standby":
		def addressFunction():
			standby_device(address)
			db = state.get_state_database()
			db[address] = action
			db.sync()
			self.refreshWidgets()
			print "got address", address, "to standby"
	return addressFunction
    def regenerateRadioWidgets(self):
	for address_status in state.get_state_database().items():
		widget = Radiobutton(self.root, variable = self.active_device, value = address_status[0])
		if get_alias(address_status[0]) == False: widget["text"] = address_status[0]
		else: widget["text"] = unicode(get_alias(address_status[0]))
		if address_status[1] == 'authorize':
			widget.select()
		if address_status[1] == 'standby':
			widget["command"] = self.generateAddressFunction(address_status[0], 'authorize')
		self.addressWidgets.append(widget)
		widget.pack({"side": "top"})
    def teardownWidgets(self):
	if hasattr(self, "addressWidgets"):
		for widget in self.addressWidgets:
			widget.destroy()
    def refreshWidgets(self):
	print "refreshing... "
	self.teardownWidgets()
	self.regenerateRadioWidgets()
    def callback(self):
       exit()
       self.root.quit()
    def run(self):
        self.root=Tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.wm_title("Bluserve")
	self.active_device = StringVar()
	self.addressWidgets = []
	self.regenerateRadioWidgets()
        self.root.mainloop()
