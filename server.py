import bottle, json, state, bluserve_library
from bluserve_library import standby_device, authorize_device
begin_html = "<html><head></head><body><form action='./set_state' method='POST'>"

def gen_li(address_action):
    if address_action[1] != 'authorize': input = "<input type='radio' name='device_address' value='%s'>" % address_action[0] +address_action[0]
    else: input = "<input type='radio' name='device_address' value='%s' checked>" % address_action[0] + address_action[0]
    return input + "<br/>"

def gen_list():
    db = state.get_state_database()
    list = ""
    for item in db.items(): list = list + gen_li(item)
    return list

end_html = "<input type='submit'></form></body></html>"
@bottle.get('/get_html')
def get_html_state():
    
    return begin_html+ gen_list() + end_html
@bottle.get('/get_json')
def get_json_state():
    return json.dumps(state.get_state_database())

def generateAddressFunction(address=None, action=None):
    if action == "authorize":
            def addressFunction():
                    db = state.get_state_database()
                    for a in db:
                           standby_device(a)
                           db[a] = 'standby'
                    authorize_device(address)
                    db[address] = action
                    db.sync()
                    print "got address", address, "to authorize"
    if action == "standby":
            def addressFunction():
                    standby_device(address)
                    db = state.get_state_database()
                    db[address] = action
                    db.sync()
                    print "got address", address, "to standby"
    return addressFunction


@bottle.post('/set_state')
def set_state():
    print bottle.request.forms.get('device_address')
    generateAddressFunction(address=bottle.request.forms.get('device_address'), action="authorize")()
    bluserve_library.daemon_function()
    return get_html_state()

bottle.run(host='192.168.2.25', port=13341, debug=True, reloader=True)

