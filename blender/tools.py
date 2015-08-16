import bpy
import math
from mathutils import Euler

SENSEL_DEVICE = None

TOOL_LIST = [
		[('VIEW_PAN', 0), ('VIEW_ROTATE', 1), ('VIEW_CURSOR', 2)],
		[('OBJECT_INDENT', 3), ('OBJECT_ROTATED', 4), ('OBJECT_MOVE', 5), ('SENSITIVITY', 6)],
		[('RESET', 10), ('UNDO', 13), ('REDO', 14)]
]

NUM_BUTTONS = 16
LED_BRIGHTNESS = 150
LED_LIST = []
for i in range(NUM_BUTTONS):
	LED_LIST.append(0)

WIDTH = 230
HEIGHT = 120

TOOL_THRESHOLD = 90
FORCE_THRESHOLD = 3000

BUTTON_WIDTH = TOOL_THRESHOLD / len(TOOL_LIST)
BUTTON_HEIGHTS = []
for column in TOOL_LIST:
	BUTTON_HEIGHTS.append(HEIGHT / len(column))

# prime doe
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
		if tool == 'RESET':
			reset()
		elif tool == 'UNDO' or tool == 'REDO':
			history(tool)
		elif selected_tool != tool:
			selected_tool = tool
			updateLED()
			print("Selecting %s at %s, %s" % (selected_tool, contacts[0].x_pos_mm, contacts[0].y_pos_mm))
		prev_coords = [contacts[0].x_pos_mm, contacts[0].y_pos_mm]
		return
	else:
		for contact in contacts:
			if contact.id is 0:
				if prev_coords[0] is 0.0:
					prev_coords = [contact.x_pos_mm, contact.y_pos_mm]
					return
				else:
					if selected_tool == 'OBJECT_MOVE':
						object_move(contact, len(contacts))
					elif selected_tool == 'OBJECT_ROTATE':
						object_rotate(contact, len(contacts))
					elif selected_tool == 'VIEW_PAN':
						view_pan(contact, len(contacts))
					elif selected_tool == 'VIEW_ROTATE':
						view_rotate(contact, len(contacts))
					prev_coords = [contact.x_pos_mm, contact.y_pos_mm]
					return

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

def flashLED(tool):
	if prev_coords == [0.0, 0.0]:
		flash_index = -1
		if tool == 'RESET':
			flash_index = 10
		elif tool == 'UNDO':
			flash_index = 13
		elif tool == 'REDO':
			flash_index = 14
		if flash_index > -1:
			LED_LIST[flash_index] = LED_BRIGHTNESS
			SENSEL_DEVICE.setLEDBrightness(LED_LIST)
			LED_LIST[flash_index] = 0
			SENSEL_DEVICE.setLEDBrightness(LED_LIST)

def reset():
	flashLED('RESET')

	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			area.spaces[0].region_3d.view_rotation = (0.8, 0.46, 0.2, 0.34)
			area.spaces[0].region_3d.view_location = (0, 0, 0)
			area.spaces[0].region_3d.view_distance = 9

	for blender_object in bpy.context.selected_objects:
		blender_object.rotation_euler = (0, 0, 0)
		blender_object.location = (0, 0, 0)

def history(tool_name):
	if tool_name == 'UNDO':
		print("Undo")
		bpy.ops.ed.undo()
		flashLED(tool_name)
	elif tool_name == 'REDO':
		print("Redo")
		bpy.ops.ed.redo()
		flashLED(tool_name)



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

def object_rotate(contact, numContacts):
	tmp_sensitivity = sensitivity - ((numContacts - 1) * 35)
	if tmp_sensitivity < 20:
		tmp_sensitivity = 20
	delta_x, delta_y = calc_delta(contact)
	delta_x /= tmp_sensitivity
	delta_y /= tmp_sensitivity
	for blender_object in bpy.context.selected_objects:
		blender_object.transform.rotation_euler = (delta_y, delta_x, 0)

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
			view_zoom(view, contact, numContacts)

def view_pan(contact, numContacts):
	for view in bpy.context.screen.areas:
		if view.type == 'VIEW_3D':
			tmp_sensitivity = sensitivity - ((numContacts - 1) * 35)
			if tmp_sensitivity < 20:
				tmp_sensitivity = 20
			delta_x, delta_y = calc_delta(contact)
			delta_x /= tmp_sensitivity
			delta_y /= tmp_sensitivity
			view.spaces[0].region_3d.view_location = (view.spaces[0].region_3d.view_location.x + delta_y,
													  view.spaces[0].region_3d.view_location.y + delta_x,
													  view.spaces[0].region_3d.view_location.z)
			view_zoom(view, contact, numContacts)

def view_zoom(view, contact, numContacts):
	direction = -1
	if numContacts > 1:
		direction = 1
	print(contact.total_force)
	if contact.total_force > FORCE_THRESHOLD:
		view.spaces[0].region_3d.view_distance += contact.total_force / 20000 * direction

def calc_delta(contact):
	delta_x = (contact.x_pos_mm - prev_coords[0])
	delta_y = (contact.y_pos_mm - prev_coords[1])
	return delta_x, delta_y