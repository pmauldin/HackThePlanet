import bpy
import sensel
import tools

class ModalTimerOperator(bpy.types.Operator):
	"""Operator which runs its self from a timer"""
	bl_idname = "wm.modal_timer_operator"
	bl_label = "Modal Timer Operator"

	_timer = None

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
			tools.process_input(contacts)

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