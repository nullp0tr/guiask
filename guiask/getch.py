import select
import sys
import tty
import termios


def getchar():
    ch = None
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch = ch + sys.stdin.read(1)
                if ch[-1] == '[':
                    ch = ch + sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == '__main__':
    while True:
        ch = getchar()
        if ch:
            print(repr(ch))
        if ch == '\x03':
            break
