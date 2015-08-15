import bpy

# surface height = 120mm
# surface width = 230mm
# tool space width = 64
TOOL_LIST = [
		['VIEW_MOVE', 'VIEW_PAN', 'VIEW_ROTATE', 'OBJECT_ROTATED'],
		['OBJECT_INDENT', 'VIEW_CURSOR', 'SENSITIVITY', 'RESET', 'PH']
	]
BUTTON_WIDTH = 120 / len(TOOL_LIST[0])
BUTTON_HEIGHT = 230 / len(TOOL_LIST[1])

WIDTH = 230
HEIGHT = 120

TOOL_THRESHOLD = 65

sensitivity = 80000
selected_tool = "PAN"

def process_inputs(contacts, selected_tool):

	for contact in contacts:
		if contact.x_pos_mm < TOOL_THRESHOLD:
			select_tool(contact)
			break
		else:
			print("Touching myself")


def select_tool(contact):
	x_coord = contact.x_pos_mm
	y_coord = contact.y_pos_mm
	print("Selecting tool at %s, %s" % (x_coord, y_coord))
	return TOOL_LIST[x_coord / BUTTON_WIDTH][y_coord / BUTTON_HEIGHT]
