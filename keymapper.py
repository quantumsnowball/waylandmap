import sys
import traceback
import evdev
import uinput
import yaml
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')


EVENTS = {k:v for k,v in vars(uinput.ev).items() if k.startswith(('KEY_', 'BTN_', 'REL_', 'ABS_', ))}
KEYS = {k:v for k,v in EVENTS.items() if k.startswith('KEY_')}


def get_event_name(value):
    keys = {v:k for k,v in EVENTS.items()}
    return keys.get(value, '')


def main():
    # parse user config file
    keymaps = None
    with open('keymaps.yaml') as f:
        keymaps = yaml.safe_load(f)
    if not keymaps:
        raise Exception('Error in reading user config file')
    # organize into swap list and map list
    swap_list = tuple((m['target1'], m['target2'])
                       for m in keymaps if m['type'] == 'swap')
    map_list = tuple((m['source'], m['target'])
                      for m in keymaps if m['type'] == 'map')
    combo_list = tuple((m['modifier'], m['source'], m['target'])
                       for m in keymaps if m['type'] == 'combo')
    # start capturing from evdev
    try:
        path = '/dev/input/event21'
        kb = evdev.InputDevice(path)
        kb.grab()
        logging.info('Device:', kb)

        with uinput.Device(KEYS.values()) as vdev:
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
                            # key mapper will record that the status of right alt
                            isRalt = value_in >= 1
                            # right alt key events are blocked
                            continue
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
                            # remap home + pgdn + pgup + end
                            if code_in == uinput.KEY_N[1]:
                                type_out, code_out = uinput.KEY_HOME
                            if code_in == uinput.KEY_M[1]:
                                type_out, code_out = uinput.KEY_PAGEDOWN
                            if code_in == uinput.KEY_COMMA[1]:
                                type_out, code_out = uinput.KEY_PAGEUP
                            if code_in == uinput.KEY_DOT[1]:
                                type_out, code_out = uinput.KEY_END
                            # remap backspace + delete
                            if code_in == uinput.KEY_Y[1]:
                                type_out, code_out = uinput.KEY_BACKSPACE
                            if code_in == uinput.KEY_U[1]:
                                type_out, code_out = uinput.KEY_BACKSPACE
                            if code_in == uinput.KEY_I[1]:
                                type_out, code_out = uinput.KEY_DELETE
                            if code_in == uinput.KEY_O[1]:
                                type_out, code_out = uinput.KEY_DELETE
                    # send back all event
                    vdev.emit((type_out, code_out), value_out)
                    # log
                    logging.info((
                        f'\tIN: ({get_event_name((type_in, code_in)):>15},T={type_in:1},C={code_in:3},V={value_in:6}), '
                        f'\tOUT: ({get_event_name((type_out, code_out)):>15},T={type_out:1},C={code_out:3},V={value_out:6}), \tisRalt: {isRalt}'))
                except KeyboardInterrupt:
                    kb.ungrab()
                    logging.error(traceback.format_exc())
                    sys.exit(0)
                
    except (PermissionError, ):
        logging.error("Must be run as sudo")


if __name__ == '__main__':
    main()

