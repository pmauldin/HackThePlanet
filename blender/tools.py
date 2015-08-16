import bpy
import math
from mathutils import Euler

SENSEL_DEVICE = None

TOOL_LIST = [
		[('VIEW_MOVE', 0), ('VIEW_PAN', 1), ('VIEW_ROTATE', 2), ('VIEW_CURSOR', 3)],
		[('OBJECT_INDENT', 4), ('OBJECT_ROTATED', 5), ('OBJECT_MOVE', 6), ('SENSITIVITY', 7), ('RESET', 8)],
		[('UNDO', 9), ('REDO', 10)]
]

NUM_BUTTONS = 11
LED_BRIGHTNESS = 150
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
selected_tool = "VIEW_ROTATE"
led_index = 2

prev_coords = [0.0, 0.0]

def process_inputs(contacts):
	global selected_tool
	global prev_coords
	global led_index

	if not contacts:
		prev_coords = [0.0, 0.0]
		return

	if contacts[0].x_pos_mm < TOOL_THRESHOLD:
		tool,led_index = select_tool(contacts[0])
		history(tool)
		if tool == 'RESET':
			reset()
			prev_coords = [contacts[0].x_pos_mm, contacts[0].y_pos_mm]
		else:
			selected_tool = tool
			updateLED()
		print("Selecting %s at %s, %s" % (selected_tool, contacts[0].x_pos_mm, contacts[0].y_pos_mm))
	else:
		for contact in contacts:
			if contact.id is 0:
				if prev_coords[0] is 0.0:
					prev_coords = [contact.x_pos_mm, contact.y_pos_mm]
					return
				else:
					if selected_tool == 'OBJECT_MOVE':
						object_move(contact, len(contacts))
					elif selected_tool == 'VIEW_ROTATE':
						view_rotate(contact, len(contacts))
					prev_coords = [contact.x_pos_mm, contact.y_pos_mm]

def set_device(device):
	global SENSEL_DEVICE
	SENSEL_DEVICE = device

def select_tool(contact):
	x = math.floor(contact.x_pos_mm / BUTTON_WIDTH)
	y = math.floor(contact.y_pos_mm / BUTTON_HEIGHTS[x])
	return TOOL_LIST[x][y]

def updateLED():
	global led_index

	if led_index == 8:
		return

	for i in range(NUM_BUTTONS):
		LED_LIST[i] = 0
	LED_LIST[led_index] = LED_BRIGHTNESS
	SENSEL_DEVICE.setLEDBrightness(LED_LIST)

def resetAlertLED():
	LED_LIST[8] = 254
	SENSEL_DEVICE.setLEDBrightness(LED_LIST)
	LED_LIST[8] = 0
	SENSEL_DEVICE.setLEDBrightness(LED_LIST)

def reset():
	if prev_coords == [0.0, 0.0]:
		resetAlertLED()
	#TODO: for loop
	bpy.context.screen.areas[2].spaces[0].region_3d.view_rotation = (0.8, 0.46, 0.2, 0.34)
	bpy.context.screen.areas[2].spaces[0].region_3d.view_location = (0, 0, 0, 0)
	bpy.context.screen.areas[2].spaces[0].region_3d.view_distance = 9
	for blender_object in bpy.context.selected_objects:
		blender_object.rotation_euler = (0, 0, 0)
		blender_object.location = (0, 0, 0)

def history(tool_name):
	if tool_name == 'UNDO':
		bpy.ops.ed.undo()
	elif tool_name == 'REDO':
		bpy.ops.ed.redo()



def object_move(contact, numContacts):
	tmp_sensitivity = sensitivity - ((numContacts - 1) * 35)
	if tmp_sensitivity < 20:
		tmp_sensitivity = 20
	delta_x, delta_y = calc_delta(contact)
	delta_x /= tmp_sensitivity
	delta_y /= tmp_sensitivity
	for blender_object in bpy.context.selected_objects:
		blender_object.location = (blender_object.location.x + delta_y,
		                           blender_object.location.y + delta_x,
		                           blender_object.location.z)

def view_rotate(contact, numContacts):
	for view in bpy.context.screen.areas:
		if view.type == 'VIEW_3D':
			tmp_sensitivity = sensitivity - ((numContacts - 1) * 35)
			if tmp_sensitivity < 20:
				tmp_sensitivity = 20
			delta_x, delta_y = calc_delta(contact)
			delta_x /= tmp_sensitivity
			delta_y /= tmp_sensitivity
			view.spaces[0].region_3d.view_rotation.rotate(Euler((0, delta_y, delta_x)))

def calc_delta(contact):
	delta_x = (contact.x_pos_mm - prev_coords[0])
	delta_y = (contact.y_pos_mm - prev_coords[1])
	return delta_x, delta_y