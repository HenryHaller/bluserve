#!/usr/bin/python
import state, dbus, threading, time

#NON SIGNAL VERSION

class registerer_thread(threading.Thread):
	def __init__(self, new_devices_event):
		threading.Thread.__init__(self)
		self.daemon=True
		self.new_devices_event=new_devices_event
		self.name = "registerer_thread"
		self.bus = dbus.SystemBus()
		self.adapter = self.bus.get_object('org.bluez', self.bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))
		self.start()
	def run(self):
		while 1:
			self.register()
			time.sleep(1)
	def register(self):
		db = state.get_state_database()
		devices = self.adapter.ListDevices(dbus_interface='org.bluez.Adapter')
		devices_list = map(lambda x: x[-17:].replace('_',':'), map(str, devices))
		for device in devices_list:
			if db.has_key(device)==False:
				print "adding "+device+" to state database"
				db[device] = "standby"
				db.sync()
				self.new_devices_event.set()
				self.new_devices_event.clear()

