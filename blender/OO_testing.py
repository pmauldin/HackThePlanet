__author__ = 'Josh'
import sys
import math
from tool import Tool

TOOLS_LIST = [
	('VIEW_PAN', 0), ('VIEW_ROTATE', 1), ('VIEW_CURSOR', 2),
	('OBJECT_MOVE', 3), ('OBJECT_ROTATE', 4), ('TOGGLE_MODE', 5),
	('RESET', 13), ('UNDO', 14), ('REDO', 15)
]


def main():
	global TOOLS_LIST
	# Tool(name, brightness, LED_index)
	bob = Tool("OBJECT_VIEW", 200, 3)
	print bob.selected
	print "Hello world"
	print bob.LED_index

	results = populate_tools(TOOLS_LIST)
	for element in results:
		print element
		print "\n"

def populate_tools(tool_list):
	results = []
	for tool in tool_list:
		results.append(Tool(tool[0], 0, tool[1]))
	return results


if __name__ == '__main__':
	main()
