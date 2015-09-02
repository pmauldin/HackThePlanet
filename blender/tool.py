__author__ = 'lakitu'
import bpy
import math
import sys

# attributes: LEDBrightness, isSelected, isActive, x loc, y loc
class Tool:
	def __init__(self, name, brightness):
		self.name = name
		self.brightness = brightness
		self.active = False
		self.selected = False

	def select(self):
		self.selected = True