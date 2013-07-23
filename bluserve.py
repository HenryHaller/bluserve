#!/usr/bin/python
import sys, threading, time
from bluserve_library import daemon_function

#do we run a GUI?
GUI=True
if "--no-gui" in sys.argv:
	GUI=False

#do we run a server?
SERVER=True
if "--no-server" in sys.argv:
	SERVER=False

#define our events
redraw_event = threading.Event()
#reselect_event = threading.Event()
daemon_function_event = threading.Event()

from bluserve_register import registerer_thread
rt = registerer_thread(redraw_event)
print "started registerer thread?"


if GUI == True:
	import gui
	app = gui.bluserve_tk(daemon_function_event)
	def new_devices_event_looper():
		while 1:
			redraw_event.wait()
			print "new device found"
			app.refreshWidgets()
	new_devices_event_looper = threading.Thread(target=new_devices_event_looper, name="new_devices_event_loop")
	new_devices_event_looper.daemon = True
	new_devices_event_looper.start()
	def reselect_event_handler():
		while 1:
			daemon_function_event.wait()
			app.reselect()
	reselect_event_handler_thread = threading.Thread(target=reselect_event_handler, name="reselector_thread")
	reselect_event_handler_thread.daemon = True
	reselect_event_handler_thread.start()

if SERVER == True:
	import server
	server = server.Server(daemon_function_event)
	server_thread = threading.Thread(target=server.start, name="server_thread")
	server_thread.daemon = True
	server_thread.start()

#handle daemon function!!!

def daemon_function_event_handler():
	while 1:
		daemon_function_event.wait()
		#df_timer=10
		daemon_function()
dfeh = threading.Thread(target=daemon_function_event_handler, name="daemon_function_event_handler")
dfeh.daemon=True
dfeh.start()

while 1: continue


#work on this later
"""
df_timer=10.0
def daemon_function_looper(df_timer):
	while True:
		if df_timer<0:
			daemon_function_event.set()
			daemon_function_event.clear()
			df_timer=10
		time.sleep(.1)
		#df_timer = df_timer-0.1
		print df_timer
df=threading.Thread(target=daemon_function_looper, name="daemon_function_event_looper")
df.daemon=True
#df.start()
"""
