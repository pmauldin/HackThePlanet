#!/usr/bin/env python

import portable_getch
import threading


_kbthread_getch = portable_getch.Getch()
_kbthread_exit_requested = False
_kbthread_read_callback = None
_kbthread = None

def _kbReadThread(callback):
    global _kbthread_exit_requested

    while not _kbthread_exit_requested:
        ch = _kbthread_getch(0.1)
        if ch:
            callback(ch)


def keyboardReadThreadStart(callback):
    global _kbthread_exit_requested
    global _kbthread

    _kbthread_exit_requested = False
    _kbthread = threading.Thread(target=_kbReadThread, 
                                 name="KB_THREAD", 
                                 args=[callback])
    _kbthread.start()

def keyboardReadThreadStop():
    global _kbthread_exit_requested

    if _kbthread:
        _kbthread_exit_requested = True
        _kbthread.join()
