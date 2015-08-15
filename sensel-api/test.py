import sensel

def read_input():
	try:
		width = 230
		height = 120
		sensel_device = sensel.SenselDevice()

		if not sensel_device.openConnection():
			print "Unable to open Sensel sensor!"
			exit()

		sensel_device.setFrameContentControl(sensel.SENSEL_FRAME_CONTACTS_FLAG)

		sensel_device.startScanning(0)

		while True:
			contacts = sensel_device.readContacts()

			for c in contacts:
				if c.x_pos_mm <= width/2:
					if c.y_pos_mm <= height/2:
						print "%s: Top-left!" % c.id
					else:
						print "%s: Bottom-left!" % c.id
				else:
					if c.y_pos_mm <= height/2:
						print "%s: Top-right!" % c.id
					else:
						print "%s: Bottom-right!" % c.id
	finally:
		sensel_device.stopScanning()
		sensel_device.closeConnection()


if __name__ == "__main__":
	read_input()