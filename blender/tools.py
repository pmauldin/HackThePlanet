import bpy

# surface height = 120mm
# surface width = 230mm
# tool space width = 64
import math

TOOL_LIST = [
		['VIEW_MOVE', 'VIEW_PAN', 'VIEW_ROTATE', 'VIEW_CURSOR'],
		['OBJECT_INDENT', 'OBJECT_ROTATED', 'SENSITIVITY', 'RESET']
]

WIDTH = 230
HEIGHT = 120

TOOL_THRESHOLD = 65

BUTTON_WIDTH = TOOL_THRESHOLD / 2
BUTTON_HEIGHT = HEIGHT / len(TOOL_LIST[0])


sensitivity = 80000
selected_tool = "VIEW_CURSOR"

def process_inputs(contacts):
	global selected_tool

	for contact in contacts:
		if contact.x_pos_mm < TOOL_THRESHOLD:
			selected_tool = select_tool(contact.x_pos_mm, contact.y_pos_mm)
			print("Selecting %s at %s, %s" % (selected_tool, contact.x_pos_mm, contact.y_pos_mm))
			break


def select_tool(xpos, ypos):
	x = math.floor(xpos / BUTTON_WIDTH)
	print (x)
	y = math.floor(ypos / BUTTON_HEIGHT)
	print (y)
	return TOOL_LIST[x][y]
