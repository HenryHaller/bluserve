import kivy
#kivy.require('1.7.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout

import net


class Layout(GridLayout):
    def generate_title(self):
	title = Label(text="Bluserve", size_hint_y=0.5)
	self.add_widget(title)
    def refresh(self, btn):
	net.set_state(btn.text)
	map(self.remove_widget, self.widgets)
	self.widgets = []
	self.regenerate_widgets()
    def regenerate_widgets(self):
	try:
		db = net.get_database_from_server()
		for address in db:
			if db[address] == "authorize": btn = ToggleButton(text=address, group="device_addresses", state="down")
			else:
				btn = ToggleButton(text=address, group="device_addresses")
				btn.bind(on_press=self.refresh)
			self.widgets.append(btn)
		map(self.add_widget, self.widgets)
	except:
		label = Label(text="Error.")
		self.add_widget(label)
    def __init__(self, **kwargs):
	super(Layout, self).__init__(**kwargs)
	self.cols=1
	self.widgets = []
	self.generate_title()
	self.regenerate_widgets()
	

class MyApp(App):


    def build(self):
        return Layout()

if __name__ == '__main__':
    MyApp().run()
