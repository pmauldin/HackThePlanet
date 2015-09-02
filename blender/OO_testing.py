__author__ = 'Josh'
import sys
import math
from tool import Tool


def main():
	# Tool(name, LEDbrightness)
	bob = Tool("OBJECT_VIEW", 200, 3)
	print bob.selected
	print "Hello world"
	print bob.LED_index



if __name__ == '__main__':
	main()
