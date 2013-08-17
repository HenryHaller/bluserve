#!/usr/bin/python
import subprocess, time
while 1:
	check_line = subprocess.check_output("tail -n1 /var/log/messages", shell=True)
	if "[pulseaudio] module-loopback.c: Sample rates too different, not adjusting (44100 vs." in check_line:
		print "ERROR DETECTED, RESTARTING BLUETOOTH!!!"
		subprocess.check_output("service bluetooth restart", shell=True)
	time.sleep(0.5)
