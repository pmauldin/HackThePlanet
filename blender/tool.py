__author__ = 'Josh'
import math
import sys


# possible attributes?
# LEDBrightness, isSelected, x and y loc as a list (so it's mutable)


class Tool:
	def __init__(self, name, brightness, led_index):
		self.name = name
		self.LED_index = led_index
		self.brightness = brightness
		self.selected = False
		self.loc = [None, None]

	def __str__(self):
		return 'Name: ' + self.name + \
		       '\nBrightness: ' + str(self.brightness) + \
				'\nIndex: ' + str(self.LED_index)

	def toggle_selected(self):
		self.selected = not self.selected
