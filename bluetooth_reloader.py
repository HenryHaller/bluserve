#!/usr/bin/python
import subprocess, time
while 1:
	check_blob = subprocess.check_output("tail -n3 /var/log/messages", shell=True)
	if "[pulseaudio] module-loopback.c: Sample rates too different, not adjusting (44100 vs." in check_blob:
		print "ERROR DETECTED, RESTARTING BLUETOOTH!!!"
		subprocess.check_output("service bluetooth restart", shell=True)
	time.sleep(0.5)
