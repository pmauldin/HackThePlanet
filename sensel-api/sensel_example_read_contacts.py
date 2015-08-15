#!/usr/bin/env python
#
#  Read Contacts
#  by Aaron Zarraga - Sensel, Inc
# 
#  This opens a Sensel sensor, reads contact data, and prints the data to the console.
#
#  Note: We have to use \r\n explicitly for print endings because the keyboard reading code
#        needs to set the terminal to "raw" mode.
##

from __future__ import print_function
from keyboard_reader import *
import sensel

exit_requested = False

def keypress_handler(ch):
    global exit_requested

    if ch == 0x51 or ch == 0x71: #'Q' or 'q'
        print("Exiting Example...", end="\r\n")
        exit_requested = True


def openSensorReadContacts():
    sensel_device = sensel.SenselDevice()

    if not sensel_device.openConnection():
        print("Unable to open Sensel sensor!", end="\r\n")
        exit()

    keyboardReadThreadStart(keypress_handler)

    #Enable contact sending
    sensel_device.setFrameContentControl(sensel.SENSEL_FRAME_CONTACTS_FLAG)
  
    #Enable scanning
    sensel_device.startScanning(0)

    print("\r\nTouch sensor! (press 'q' to quit)...", end="\r\n")

    while not exit_requested: 
        contacts = sensel_device.readContacts()
  
        if contacts == None:
            print("NO CONTACTS", end="\r\n")
            continue
   
        for c in contacts:
            event = ""
            if c.type == sensel.SENSEL_EVENT_CONTACT_INVALID:
                event = "invalid"
            elif c.type == sensel.SENSEL_EVENT_CONTACT_START:
                event = "start"
            elif c.type == sensel.SENSEL_EVENT_CONTACT_MOVE:
                event = "move"
            elif c.type == sensel.SENSEL_EVENT_CONTACT_END:
                event = "end"
            else:
                event = "error"
    
            print("Contact ID %d, event=%s, mm coord: (%f, %f), force=%d" % 
                  (c.id, event, c.x_pos_mm, c.y_pos_mm, c.total_force), end="\r\n")

        if len(contacts) > 0:
            print("****", end="\r\n");

    sensel_device.stopScanning();
    sensel_device.closeConnection();
    keyboardReadThreadStop()

if __name__ == "__main__":
    openSensorReadContacts()
    
