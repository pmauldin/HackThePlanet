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
	return TOOL_LIST[int(contact.x_pos_mm / BUTTON_WIDTH)][int(contact.y_pos_mm / BUTTON_HEIGHT)]
