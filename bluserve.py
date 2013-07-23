#!/usr/bin/python
import sys, threading

if "--no-gui" not in sys.argv:
	import gui
	app = gui.bluserve_tk()

while 1: continue

"""
print 'now can continue running code while mainloop runs'

def daemon_function_looper():
	daemon_function()
	sleep_count=0
	while True:
		if sleep_count>10**3:
			daemon_function()
			sleep_count=0
		time.sleep(.01)
		sleep_count = sleep_count+1

df=threading.Thread(target=daemon_function_looper, name="MakeItWorkDaemonThread")
df.daemon=True
df.start()

#registerer_thread = bluserve_registerer()

print 'still alive?'


from bluserve_register2 import registerer_thread
new_devices_event = threading.Event()
rt = registerer_thread(new_devices_event)
print "started registerer thread?"


def new_devices_event_looper():
	new_devices_event.wait()
	print "new device found"
	app.refreshWidgets()
new_devices_event_looper = threading.Thread(target=new_devices_event_looper, name="new_devices_event_loop")
new_devices_event_looper.daemon = True
new_devices_event_looper.start()


while 1: continue

"""
