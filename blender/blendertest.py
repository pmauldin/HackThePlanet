import bpy
import sensel

class ModalTimerOperator(bpy.types.Operator):
	"""Operator which runs its self from a timer"""
	bl_idname = "wm.modal_timer_operator"
	bl_label = "Modal Timer Operator"

	_timer = None

	width = 230
	height = 120

	sensitivity = 80000

	sensel_device = sensel.SenselDevice()
	sensel_device.openConnection()

	sensel_device.setFrameContentControl(sensel.SENSEL_FRAME_CONTACTS_FLAG)

	sensel_device.startScanning(0)

	def modal(self, context, event):
		if event.type in {'ESC'}:
			self.cancel(context)
			return {'CANCELLED'}

		if event.type == 'TIMER':
			contacts = self.sensel_device.readContacts()

			for contact in contacts:
				if contact.x_pos_mm <= self.width/2:
					if contact.y_pos_mm <= self.height/2:
						print("Decreasing x")
						# if contact.total_force > 2000:
						bpy.context.selected_objects[0].location.x -= contact.total_force/self.sensitivity
					else:
						print ("Increasing X")
						# if contact.total_force > 2000:
						bpy.context.selected_objects[0].location.x += contact.total_force/self.sensitivity
				else:
					if contact.y_pos_mm <= self.height/2:
						print ("Increasing Z")
						# if contact.total_force > 2000:
						bpy.context.selected_objects[0].location.z += contact.total_force/self.sensitivity
					else:
						print ("Decreasing z")
						# if contact.total_force > 2000:
						bpy.context.selected_objects[0].location.z -= contact.total_force/self.sensitivity

		return {'PASS_THROUGH'}

	def execute(self, context):
		wm = context.window_manager
		self._timer = wm.event_timer_add(0.001, context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}

	def cancel(self, context):
		print("Stopping...")
		self.sensel_device.stopScanning()
		self.sensel_device.closeConnection()
		wm = context.window_manager
		wm.event_timer_remove(self._timer)


def register():
	bpy.utils.register_class(ModalTimerOperator)


def unregister():
	bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
	register()

	# test call
	bpy.ops.wm.modal_timer_operator()
