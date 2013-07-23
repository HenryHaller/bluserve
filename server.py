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






"""
server = bottle.Bottle()


#bottle.run(host='192.168.2.25', port=13341, debug=True, reloader=True)

"""


class Server:
    def __init__(self, daemon_function_event, host, port):
        self._host = host
        self._port = port
	self.daemon_function_event = daemon_function_event
        self._app = bottle.Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self.get_html_state)
        self._app.route('/get_json', method="GET", callback=self.get_json_state)
        self._app.route('/set_state', method="POST", callback=self.set_state)
#        self._app.route('/hello/<name>', callback=self._hello)
#@server.get('/get_html')

    def get_html_state(self):
        return begin_html+ gen_list() + end_html
#@server.get('/get_json')

    def get_json_state(self):
        return json.dumps(state.get_state_database())

    def AddressFunction(self, address=None):
        db = state.get_state_database()
        for a in db: db[a] = 'standby'
        db[address] = 'authorize'
        db.sync()

    def set_state(self):
        print "received remote request to authorize "+bottle.request.forms.get('device_address')
        self.AddressFunction(address=bottle.request.forms.get('device_address'))
	self.daemon_function_event.set()
	self.daemon_function_event.clear()
        return self.get_html_state()

    def start(self):
        self._app.run(host=self._host, port=self._port)


#    def _hello(self, name="Guest"):
#       return template('Hello {{name}}, how are you?', name=name)

#server = Server(host='localhost', port=8090)
#server.start()
