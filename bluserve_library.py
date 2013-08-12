#!/usr/bin/python
import state, time, subprocess, dbus, sys
bus = dbus.SystemBus()
adapter = bus.get_object('org.bluez', bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))

def get_device(address):
    try:
        device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
    except:
        sys.stderr.write( "no device path for "+address+"\n")
        sys.stderr.write( "error "+ str(sys.exc_info()[0])+"\n")
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
        return device_object
    except:
	sys.stderr.write( "error getting device_object for "+address+"\n")
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
        sys.stderr.write( "no device path for "+address+"\n")
        sys.stderr.write( "error "+ str(sys.exc_info()[0])+"\n")
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
        properties = device_object.GetProperties(dbus_interface="org.bluez.AudioSource")
        sys.stderr.write( address+" is "+properties['State']+"\n")
        if properties['State'] in ['connected', 'playing', 'connecting']: return True
        sys.stderr.write( device_object.Connect(dbus_interface="org.bluez.AudioSource")+"\n")
        return True
    except:
        sys.stderr.write( "error calling Connect() to %s..." % address + "\n")
        return False

def disconnect_audioSource(address):
    bus = dbus.SystemBus()
    adapter = bus.get_object('org.bluez', bus.get_object('org.bluez', '/').DefaultAdapter(dbus_interface='org.bluez.Manager'))
    try:
        device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
    except:
        sys.stderr.write( "no device path for "+address)
        sys.stderr.write( "error "+ str(sys.exc_info()[0]))
        return False
    try:
        device_object = bus.get_object('org.bluez', device_path)
    except:
        sys.stderr.write( "error finding object for address %s..." % address)
        return False
    try:
        properties = device_object.GetProperties(dbus_interface="org.bluez.AudioSource")
    except:
        sys.stderr.write( "could not get properties")
        return False
    try:
        sys.stderr.write( address+" is "+properties['State']+ "\n")
        if properties['State'] in ['disconnected']: return True
        sys.stderr.write( device_object.Disconnect(dbus_interface="org.bluez.AudioSource"))
        return True
    except:
        sys.stderr.write( "something went wrong here")
        return False

def authorize_device(address):
    #sys.stderr.write( "authorizing " + address
    #what relevant modules are there...
    device_modules = [] # should only be 1
    loopback_modules = [] # should only be 0 or 1
    for module in subprocess.check_output("pactl list modules", shell=True).split('\n\n'):
	if module.split('\n\t')[1][6:] == "module-bluetooth-device" and address.replace(':', '_') in module:
            #sys.stderr.write( module
            device_modules.append(module)
        if module.split('\n\t')[1][6:] == "module-loopback" and address.replace(':', '_') in module:
            #sys.stderr.write( module
            loopback_modules.append(module)
    if len(loopback_modules) == 0:
        #no loop back module... 
	# is there a device module?
	if len(device_modules) == 0:
            try:
		sys.stderr.write( "about to call connect_audioSource \n")
                if connect_audioSource(address) == False: return False
            except:
                sys.stderr.write( "caught an error trying to AudioSource.Connect() to " + address)
            try:
                device_path = adapter.FindDevice(address, dbus_interface='org.bluez.Adapter')
            except:
                sys.stderr.write( "had an error trying to find a device for address " + address+"\n")
                sys.stderr.write( "device_address is " + address+"\n")
                sys.stderr.write( "cannot continue successfully unless bluez sees the device \n")
                return
            #command = "pactl load-module module-bluetooth-device address=%s path=%s profile=a2dp_source auto_connect=no" % (address, device_path)
            #try:
            #    subprocess.check_output(command, shell=True)
            #except:
            #    sys.stderr.write( "failed to create a bluetooth-device module for " + address
            #    return False
        #if no device module, lets assume no source either...
	#create loopback a module
        try:
            sinks_info = subprocess.check_output(["pactl", "list", "short", "sinks"]).split("\n")  # ugly
            sink = sinks_info[0].split("\t")[1]
            source = "bluez_source." + address.replace(':', '_')
            command = "pactl load-module module-loopback source_dont_move=yes source=%s sink=%s" % (source, sink)
            sys.stderr.write( "connecting"+ source+ "to"+ sink+"\n")
            subprocess.check_output(command, shell=True)
        except:
            sys.stderr.write( "failed to create a loopback module for " + address +"\n")
    return True

def standby_device(address):
    #sys.stderr.write( "putting on standby " + address
    device_modules = []
    for module in subprocess.check_output("pactl list modules", shell=True).split('\n\n'):
        if module.split('\n\t')[1][6:] == "module-bluetooth-device" and address.replace(':', '_') in module:
            module_index = module.split('\n\t')[0][8:]
            command = "pactl unload-module " + module_index
            try: subprocess.check_output(command, shell=True)
            except: sys.stderr.write( "error unloading module "+module_index)
    disconnect_audioSource(address)

def reject_device(address):
    sys.stderr.write( "rejecting " + address)
#unload modules and disconnect as sink

def daemon_function():
    #sys.stderr.write( "executing daemon_function\n")
    modules = subprocess.check_output("pactl list modules", shell=True).split('\n\n')
    db = state.get_state_database()
    sys.stderr.write( str(db)+"\n")
    for address in db:
        if db[address] == 'authorize':
            if authorize_device(address) == False:
                sys.stderr.write( "authorizing %s failed\n" % address)
        if db[address] == 'standby':
            standby_device(address)
        if db[address] == 'reject':
            reject_device(address)
    print
