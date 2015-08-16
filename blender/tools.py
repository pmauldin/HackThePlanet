import bpy
import math
import sys
import paramiko
from mathutils import Euler

# sys.path.append("/home/peter/Hackathons/venv/lib/python3.4/site-packages/")
sys.path.append("/home/lakitu/bin/blender-2.75a-linux-glibc211-x86_64/2.7.5/python/lib/python3.4/site-packages/")
sys.path.append("/home/lakitu/.local/lib/python2.7/site-packages/")
# sys.path.append("/home/bin/blender-2.75a-linux-glibc211-x86_64/2.7.5/python/lib/python3.4/site-packages/")
from pymouse import PyMouse

SENSEL_DEVICE = None

TOOL_LIST = [
		[('VIEW_PAN', 0), ('VIEW_ROTATE', 1), ('VIEW_CURSOR', 2)],
		[('OBJECT_INDENT', 3), ('OBJECT_ROTATE', 4), ('OBJECT_MOVE', 5)],
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
FORCE_SENSITIVITY = 20000

BUTTON_WIDTH = TOOL_THRESHOLD / len(TOOL_LIST)
BUTTON_HEIGHTS = []
for column in TOOL_LIST:
	BUTTON_HEIGHTS.append(HEIGHT / len(column))

# prime doe
sensitivity = 101
selected_tool = "VIEW_PAN"
led_index = 0

prev_coords = [0.0, 0.0]

mouse = PyMouse()

def process_inputs(contacts):
	global selected_tool
	global prev_coords
	global led_index

	if not contacts:
		prev_coords = [0.0, 0.0]
		return

	if contacts[0].x_pos_mm < TOOL_THRESHOLD:
		tool, led_index = select_tool(contacts[0])
		if tool == 'RESET':
			if prev_coords == [0.0, 0.0]:
				reset()
		elif tool == 'UNDO' or tool == 'REDO':
			if prev_coords == [0.0, 0.0]:
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
					elif selected_tool == 'VIEW_CURSOR':
						view_cursor(contact, len(contacts))
					elif selected_tool == 'SCULPT_TOGGLE':
						sculpt_toggle()
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

	for i in range(NUM_BUTTONS):
		LED_LIST[i] = 0
	LED_LIST[led_index] = LED_BRIGHTNESS
	SENSEL_DEVICE.setLEDBrightness(LED_LIST)

def flashLED(tool):
	print(tool)
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

	bpy.context.scene.cursor_location = (0, 0, 0)
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
		bpy.ops.ed.undo()
		flashLED(tool_name)
	elif tool_name == 'REDO':
		bpy.ops.ed.redo()
		flashLED(tool_name)



def object_move(contact, numContacts):
	delta_x, delta_y = calc_delta(contact, numContacts)
	delta_z = calc_force(contact, numContacts)
	bpy.ops.transform.translate(value=(delta_y, delta_x, delta_z))

def object_rotate(contact, numContacts):
	delta_x, delta_y = calc_delta(contact, numContacts)
	bpy.ops.transform.rotate(value=delta_y, axis=(1,1,0))
	bpy.ops.transform.rotate(value=delta_x, axis=(0,0,1))
	for view in bpy.context.screen.areas:
		if view.type == 'VIEW_3D':
			view_zoom(view, contact, numContacts)

def view_rotate(contact, numContacts):
	for view in bpy.context.screen.areas:
		if view.type == 'VIEW_3D':
			delta_x, delta_y = calc_delta(contact, numContacts)
			view.spaces[0].region_3d.view_rotation.rotate(Euler((0, delta_y, delta_x)))
			view_zoom(view, contact, numContacts)

def view_pan(contact, numContacts):
	for view in bpy.context.screen.areas:
		if view.type == 'VIEW_3D':
			delta_x, delta_y = calc_delta(contact, numContacts)
			view.spaces[0].region_3d.view_location = (view.spaces[0].region_3d.view_location.x + delta_y,
													  view.spaces[0].region_3d.view_location.y + delta_x,
													  view.spaces[0].region_3d.view_location.z)
			view_zoom(view, contact, numContacts)

def view_zoom(view, contact, numContacts):
	delta_z = calc_force(contact, numContacts)
	view.spaces[0].region_3d.view_distance += delta_z

def view_cursor(contact, numContacts):
	TOUCH_WIDTH = WIDTH - TOOL_THRESHOLD

	w, h = mouse.screen_size()

	area = bpy.context.screen.areas[2]

	width_percent = (contact.x_pos_mm - TOOL_THRESHOLD) / TOUCH_WIDTH
	height_percent = contact.y_pos_mm / HEIGHT

	viewport_x = bpy.context.window.x + area.x
	viewport_y = h - (area.height + area.y)

	input_x = width_percent * area.width
	input_y = height_percent * area.height

	mouse.click(int(viewport_x + input_x), int(viewport_y + input_y), 1)


	delta_z = calc_force(contact, numContacts, 4500)

	if delta_z != 0:
		xx, yy = mouse.position()
		mouse.click(xx, yy, 2)

def sculpt_toggle():
	bpy.ops.object.mode_set(MODE='EDIT')

def calc_delta(contact, numContacts, base_sensitivity=35, min_sensitivity=20):
	tmp_sensitivity = sensitivity - ((numContacts - 1) * base_sensitivity)
	if tmp_sensitivity < min_sensitivity:
		tmp_sensitivity = min_sensitivity
	delta_x = (contact.x_pos_mm - prev_coords[0]) / tmp_sensitivity
	delta_y = (contact.y_pos_mm - prev_coords[1]) / tmp_sensitivity
	return delta_x, delta_y

def calc_force(contact, numContacts, threshold=FORCE_THRESHOLD):
	direction = -1
	if numContacts > 1:
		direction = 1

	force = 0
	if contact.total_force > threshold:
		force = contact.total_force / FORCE_SENSITIVITY * direction

	return force

def click():
	mouse_pos = mouse.position()
	mouse.click()

	mouse.move(mouse_pos.x, mouse_pos.yr)
