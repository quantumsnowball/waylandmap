import sys
import traceback
import evdev
import uinput
import logging


logging.basicConfig(level=logging.DEBUG)


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
                type_in, code_in, value_in = ev.type, ev.code, ev.value
                type_out, code_out, value_out = type_in, code_in, value_in
                try:
                    # only interested in key event, ignore sync event
                    if type_in == 1:
                        # check for modifier key
                        if code_in == uinput.KEY_RIGHTALT[1]:
                            isRalt = value_in >= 1
                        # do remapping here
                        if isRalt:
                            # remap alt + hjkl
                            if code_in == uinput.KEY_K[1]:
                                type_out, code_out = uinput.KEY_UP
                            if code_in == uinput.KEY_J[1]:
                                type_out, code_out = uinput.KEY_DOWN
                            if code_in == uinput.KEY_H[1]:
                                type_out, code_out = uinput.KEY_LEFT
                            if code_in == uinput.KEY_L[1]:
                                type_out, code_out = uinput.KEY_RIGHT
                            # remap home + end
                            if code_in == uinput.KEY_N[1]:
                                type_out, code_out = uinput.KEY_HOME
                            if code_in == uinput.KEY_M[1]:
                                type_out, code_out = uinput.KEY_END
                            # fake the OS right alt key is released
                            vdev.emit(uinput.KEY_RIGHTALT, 0)
                        # send back all event
                        vdev.emit((type_out, code_out), value_out)
                    logging.debug(('-----\n'
                        f'\ttype_in: {type_in}, \tcode_in: {code_in}, \tvalue: {value_in}, '
                        f'\ttype_out: {type_out}, \tcode_out: {code_out}, \tvalue_out: {value_out}, \tisRalt: {isRalt}'))
                except KeyboardInterrupt:
                    kb.ungrab()
                    print(traceback.format_exc())
                    sys.exit(0)
                
    except (PermissionError, ):
        print("Must be run as sudo")


if __name__ == '__main__':
    main()

