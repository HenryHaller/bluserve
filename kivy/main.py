import kivy
#kivy.require('1.7.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout

import net

class Layout(GridLayout):
    def generateButtonFunction(self, address):
	def ButtonFunction(address):
		net.set_state(address)
	return ButtonFunction
    def regenerate_widgets(self):
	db = net.get_database_from_server()
	for address in db:
		if db[address] == "authorize": btn = ToggleButton(text=address, group="device_addresses", state="down")
		else: btn = ToggleButton(text=address, group="device_addresses")
		btn.bind(on_press=self.generateButtonFunction(address))
		self.add_widget(btn)
    def __init__(self, **kwargs):
	super(Layout, self).__init__(**kwargs)
	self.cols=1
	self.regenerate_widgets()
	

class MyApp(App):


    def build(self):
        return Layout()

if __name__ == '__main__':
    MyApp().run()
