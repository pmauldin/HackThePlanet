#From stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
#Aaron added code for timeout support

class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self, timeout): return self.impl(timeout)


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self, timeout):
        import sys, tty, termios
        from select import select

        ch = None
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select([sys.stdin], [], [], timeout)

            if rlist:
                ch = ord(sys.stdin.read(1))
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self, timeout):
        import msvcrt, time, sys

        start_time = time.time()
        ch = None

        while True:
            if msvcrt.kbhit():
                ch = ord(msvcrt.getch())
                break
            elif time.time() - start_time > timeout:
                break

        return ch
