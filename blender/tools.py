import bpy

# surface height = 120mm
# surface width = 230mm
# tool space width = 64
import math
# TOOL_LIST[2][x]
TOOL_LIST = [
		[('VIEW_MOVE', 0), ('VIEW_PAN', 1), ('VIEW_ROTATE', 2), ('VIEW_CURSOR', 3)],
		[('OBJECT_INDENT', 4), ('OBJECT_ROTATED', 5), ('OBJECT_MOVE', 6), ('SENSITIVITY', 7), ('RESET', 8)]
]

NUM_BUTTONS = 8
LED_LIST = []
for i in range(NUM_BUTTONS):
	LED_LIST.append(0)

WIDTH = 230
HEIGHT = 120

TOOL_THRESHOLD = 65

BUTTON_WIDTH = TOOL_THRESHOLD / len(TOOL_LIST)
BUTTON_HEIGHTS = []
for column in TOOL_LIST:
	BUTTON_HEIGHTS.append(HEIGHT / len(column))


sensitivity = 101
selected_tool = "OBJECT_MOVE"

prev_coords = [0.0, 0.0]

def process_inputs(contacts):
	global selected_tool
	global prev_coords

	if not contacts:
		prev_coords = [0.0, 0.0]
		return

	if contacts[0].x_pos_mm < TOOL_THRESHOLD:
		tool = select_tool(contacts[0])
		if tool is 'RESET':
			reset()
		else:
			selected_tool = tool
			updateLED()
		print("Selecting %s at %s, %s" % (selected_tool, contacts[0].x_pos_mm, contacts[0].y_pos_mm))
	else:
		for contact in contacts:
			if contact.id is 0:
				if selected_tool is 'OBJECT_MOVE':
					if prev_coords[0] is 0.0:
						prev_coords = [contact.x_pos_mm, contact.y_pos_mm]
					else:
						# print ("Prev coords: [%d, %d]  -  Current coords [%d, %d]" % (prev_coords[0], prev_coords[1], contact.x_pos_mm, contact.y_pos_mm))
						object_move(contact, len(contacts))
						prev_coords = [contact.x_pos_mm, contact.y_pos_mm]
					return

def select_tool(contact):
	x = math.floor(contact.x_pos_mm / BUTTON_WIDTH)
	y = math.floor(contact.y_pos_mm / BUTTON_HEIGHTS[x])
	print (str(x) + "   " + str(y))
	return TOOL_LIST[x][y]

def updateLED():
	global index
	for i in range(NUM_BUTTONS):
		LED_LIST[i] = 0
	LED_LIST[index] = 255

def reset():
	for blender_object in bpy.context.selected_objects:
		blender_object.rotation_euler = (0, 0, 0)
		blender_object.location = (0, 0, 0)

def object_move(contact, numContacts):
	tmp_sensitivity = sensitivity - ((numContacts - 1) * 35)
	if tmp_sensitivity < 20:
		tmp_sensitivity = 20
	delta_x = (contact.x_pos_mm - prev_coords[0]) / tmp_sensitivity
	delta_y = (contact.y_pos_mm - prev_coords[1]) / tmp_sensitivity
	print (tmp_sensitivity)
	for blender_object in bpy.context.selected_objects:
		blender_object.location = (blender_object.location.x + delta_y,
		                           blender_object.location.y + delta_x,
		                           blender_object.location.z)
