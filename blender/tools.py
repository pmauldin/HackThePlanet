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
			selected_tool = select_tool(contact)
			print("Selecting %s at %s, %s" % (selected_tool, contact.x_pos_mm, contact.y_pos_mm))
			break
		else:
			print("Touching myself")


def select_tool(contact):
	x = math.floor(contact.x_pos_mm / BUTTON_WIDTH)
	y = math.floor(contact.y_pos_mm / BUTTON_HEIGHT)
	return TOOL_LIST[x][y]
