import bpy

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
	print("Selecting tool at %s, %s" % (contact.x_pos_mm, contact.y_pos_mm))
