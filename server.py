import bottle, json, state, bluserve_library
from bluserve_library import standby_device, authorize_device
begin_html = "<html><head></head><body><form action='./set_state' method='POST'>"

def gen_li(address_action):
    if address_action[1] != 'authorize':
	input = "<li class='input'><input type='radio' name='device_address' value='%s' id='%s'>" % (address_action[0], address_action[0])
        input += "<label for='%s'>" % address_action[0] +  bluserve_library.get_alias(address_action[0]) + "</label>"
    else:
	input = "<li class='input selected'><input type='radio' name='device_address' value='%s' id='%s' checked>" % (address_action[0], address_action[0])
        input += "<label for='%s'>" % address_action[0] +  bluserve_library.get_alias(address_action[0]) + "</label>"
    return input + "</li>"

def gen_list():
    db = state.get_state_database()
    list = ""
    for item in db.items(): list = list + gen_li(item)
    return "<ul id='choices_list'>" + list + "</ul>"

end_html = "<input type='submit'></form></body></html>"

BASE_CSS_FILE = "/home/pi/bluserve/static/base.css"
TEMPLATE_HTML_FILE = "/home/pi/bluserve/templates/home.html"

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
	self._app.route('/static/base.css', method="GET", callback=self.base_css)
	self._app.route('/get_alias_for_address', method="POST", callback=self.get_alias_for_addres)

    def base_css(self):
	return open(BASE_CSS_FILE).read()

    def get_html_state(self):
        return bottle.template(open(TEMPLATE_HTML_FILE).read(), form_items_html=gen_list())

    def get_json_state(self):
        return json.dumps(state.get_state_database())

    def get_alias_for_addres(self):
	if len(bottle.request.forms.get('device_address')) == 17:
		alias = bluserve_library.get_alias(bottle.request.forms.get('device_address'))
		return alias

    def AddressFunction(self, address=None): #saves change of state
        db = state.get_state_database()
        for a in db: db[a] = 'standby'
        db[address] = 'authorize'
        db.sync()

    def set_state(self):
        print "received remote request to authorize "+bottle.request.forms.get('device_address')
	if len(bottle.request.forms.get('device_address')) == 17:
	        self.AddressFunction(address=bottle.request.forms.get('device_address'))
		self.daemon_function_event.set()
		self.daemon_function_event.clear()
        return self.get_html_state()

    def start(self):
        self._app.run(host=self._host, port=self._port)


