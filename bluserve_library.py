#!/usr/bin/python
import state, time, subprocess, dbus, sys
bus = dbus.SystemBus()
adapter = bus.get_object('org.bluez', bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))

def get_device(address):
    try:
        device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
    except:
        print "no device path for "+address
        print "error "+ str(sys.exc_info()[0])
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
        return device_object
    except:
	print "error getting device_object for "+address
	return False

def get_alias(address):
	device_object = get_device(address)
	if device_object != False: return device_object.GetProperties(dbus_interface="org.bluez.Device")["Alias"]
	else: return False

def connect_audioSource(address):
    bus = dbus.SystemBus()
    adapter = bus.get_object('org.bluez', bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))
    try:
        device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
    except:
        print "no device path for "+address
        print "error "+ str(sys.exc_info()[0])
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
        properties = device_object.GetProperties(dbus_interface="org.bluez.AudioSource")
        print address+" is "+properties['State']
        if properties['State'] in ['connected', 'playing', 'connecting']: return True
        print device_object.Connect(dbus_interface="org.bluez.AudioSource")
        return True
    except:
        print "error calling Connect() to %s..." % address
        return False

def disconnect_audioSource(address):
    bus = dbus.SystemBus()
    adapter = bus.get_object('org.bluez', bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))
    try:
        device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
    except:
        print "no device path for "+address
        print "error "+ str(sys.exc_info()[0])
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
    except:
        print "error finding object for address %s..." % address
        return False
    try:
        properties = device_object.GetProperties(dbus_interface="org.bluez.AudioSource")
    except:
        print "could not get properties"
        return False
    try:
        print address+" is "+properties['State']
        if properties['State'] in ['disconnected']: return True
        print device_object.Disconnect(dbus_interface="org.bluez.AudioSource")
        return True
    except:
        print "something went wrong here"
        return False

def authorize_device(address):
    print "authorizing " + address
    #what relevant modules are there...
    device_modules = [] # should only be 1
    loopback_modules = [] # should only be 0 or 1
    for module in subprocess.check_output("pactl list modules", shell=True).split('\n\n'):
	if module.split('\n\t')[1][6:] == "module-bluetooth-device" and address.replace(':', '_') in module:
            #print module
            device_modules.append(module)
        if module.split('\n\t')[1][6:] == "module-loopback" and address.replace(':', '_') in module:
            #print module
            loopback_modules.append(module)
    if len(loopback_modules) == 0:
        #no loop back module... 
	# is there a device module?
	if len(device_modules) == 0:
            try:
		print "about to call connect_audioSource ",
                if connect_audioSource(address) == False: return False
            except:
                print "caught an error trying to AudioSource.Connect() to " + address
            try:
                device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
            except:
                print "had an error trying to find a device for address " + address
                print "device_address is " + address
                print "cannot continue successfully unless bluez sees the device"
                return
            #command = "pactl load-module module-bluetooth-device address=%s path=%s profile=a2dp_source auto_connect=no" % (address, device_path)
            #try:
            #    subprocess.check_output(command, shell=True)
            #except:
            #    print "failed to create a bluetooth-device module for " + address
            #    return False
        #if no device module, lets assume no source either...
	#create loopback a module
        try:
            sinks_info = subprocess.check_output(["pactl", "list", "short", "sinks"]).split("\n")  # ugly
            sink = sinks_info[0].split("\t")[1]
            source = "bluez_source." + address.replace(':', '_')
            command = "pactl load-module module-loopback source_dont_move=yes source=%s sink=%s" % (source, sink)
            print "connecting", source, "to", sink
            subprocess.check_output(command, shell=True)
        except:
            print "failed to create a loopback module for " + address
    return True

def standby_device(address):
    print "putting on standby " + address
    device_modules = []
    for module in subprocess.check_output("pactl list modules", shell=True).split('\n\n'):
        if module.split('\n\t')[1][6:] == "module-bluetooth-device" and address.replace(':', '_') in module:
            module_index = module.split('\n\t')[0][8:]
            command = "pactl unload-module " + module_index
            try: subprocess.check_output(command, shell=True)
            except: print "error unloading module "+module_index
    disconnect_audioSource(address)

def reject_device(address):
    print "rejecting " + address
#unload modules and disconnect as sink

def daemon_function():
    print "executing daemon_function"
    modules = subprocess.check_output("pactl list modules", shell=True).split('\n\n')
    db = state.get_state_database()
    print "handling " + str(db.keys())
    for address in db:
        if db[address] == 'authorize':
            if authorize_device(address) == False:
                print "authorizing %s failed" % address
        if db[address] == 'standby':
            standby_device(address)
        if db[address] == 'reject':
            reject_device(address)
    print
