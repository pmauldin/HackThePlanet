import bpy

# surface height = 120mm
# surface width = 230mm
# tool space width = 64
import math

TOOL_LIST = [
		['VIEW_MOVE', 'VIEW_PAN', 'VIEW_ROTATE', 'VIEW_CURSOR'],
		['OBJECT_INDENT', 'OBJECT_ROTATED', 'OBJECT_MOVE', 'SENSITIVITY', 'RESET']
]

WIDTH = 230
HEIGHT = 120

TOOL_THRESHOLD = 65

BUTTON_WIDTH = TOOL_THRESHOLD / 2
BUTTON_HEIGHT = HEIGHT / len(TOOL_LIST[0])


sensitivity = 80000
selected_tool = "OBJECT_MOVE"

prev_coords = [0.0, 0.0]

def process_inputs(contacts):
	global selected_tool
	global prev_coords

	if not contacts:
		prev_coords = [0, 0]
		return

	for contact in contacts:
		if contact.x_pos_mm < TOOL_THRESHOLD:
			selected_tool = select_tool(contact)
			tool = select_tool(contact)
			if tool is 'RESET':
				reset()
			else:
				selected_tool = tool
			print("Selecting %s at %s, %s" % (selected_tool, contact.x_pos_mm, contact.y_pos_mm))
			break
		else:
			if selected_tool is 'OBJECT_MOVE':
				print ("Prev coords: [%d, %d]  -  Current coords [%d, %d]" % (prev_coords[0], prev_coords[1], contact.x_pos_mm, contact.y_pos_mm))
				prev_coords = [contact.x_pos_mm, contact.y_pos_mm]


def select_tool(contact):
	x = math.floor(contact.x_pos_mm / BUTTON_WIDTH)
	y = math.floor(contact.y_pos_mm / BUTTON_HEIGHT)
	return TOOL_LIST[x][y]

def reset():
	for blender_object in bpy.context.selected_objects:
		blender_object.rotation_euler = (0, 0, 0)
		blender_object.location = (0, 0, 0)
