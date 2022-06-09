import sys
import traceback
import evdev
import uinput


KEYS = {k:v
        for k,v in uinput.__dict__.items() 
        if k.startswith('KEY_')}


KEY_VALUES = list(KEYS.values())


def get_key_name(value):
    keys = {v:k for k,v in KEYS.items()}
    return keys[value]


def main():
    try:
        path = '/dev/input/event20'
        kb = evdev.InputDevice(path)
        print('using device:', kb)
        kb.grab()

        with uinput.Device(KEY_VALUES) as vdev:
            # keep track of if alt is press in last loop
            isRalt = False
            for ev in kb.read_loop():
                # look at each event
                type, code, value = ev.type, ev.code, ev.value
                try:
                    # only change key press down event
                    if type == 1:
                        # check for modifier key
                        if code == uinput.KEY_RIGHTALT[1]:
                            isRalt = value >= 1
                        # do remapping here
                        if isRalt:
                            # remap alt + hjkl
                            if code == uinput.KEY_K[1]:
                                type, code = uinput.KEY_UP
                            if code == uinput.KEY_J[1]:
                                type, code = uinput.KEY_DOWN
                            if code == uinput.KEY_H[1]:
                                type, code = uinput.KEY_LEFT
                            if code == uinput.KEY_L[1]:
                                type, code = uinput.KEY_RIGHT
                            # remap home + end
                            if code == uinput.KEY_N[1]:
                                type, code = uinput.KEY_HOME
                            if code == uinput.KEY_M[1]:
                                type, code = uinput.KEY_END
                            # fake the OS right alt key is released
                            vdev.emit(uinput.KEY_RIGHTALT, 0)
                        # print(f'\t\ttype: {type}, code: {code}, value: {value}, isRalt: {isRalt}')
                        vdev.emit((type, code), value)
                    print(f'\t\ttype: {type}, \tcode: {code}, \tvalue: {value}')
                except KeyboardInterrupt:
                    kb.ungrab()
                    print(traceback.format_exc())
                    sys.exit(0)
                
    except (PermissionError, ):
        print("Must be run as sudo")


if __name__ == '__main__':
    main()

