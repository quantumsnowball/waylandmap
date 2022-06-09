import sys
import traceback
import evdev
import uinput
import logging
from waylandmap.filter import Filter
from waylandmap.constants import KEYS_VALUE_TUPLE, code_to_name


def run(device, keymaps):
    filter = Filter(keymaps)
    # start capturing from evdev
    try:
        kb = evdev.InputDevice(device)
        kb.grab()

        with uinput.Device(KEYS_VALUE_TUPLE) as vdev:
            # loop to capture every event
            for ev in kb.read_loop():
                # each event represented by three ints
                type_in, code_in, value_in = ev.type, ev.code, ev.value
                try:
                    # ask filter to for correct mapping
                    result = filter.target(type_in, code_in, value_in)
                    # this key is a registered modifier key
                    if result is None:
                        # drop the event and move on to next
                        continue
                    # emit the event to OS
                    vdev.emit(*result)
                    # log
                    (type_out, code_out), value_out = result
                    name_in = code_to_name(code_in) if type_in == 1 else ''
                    name_out = code_to_name(code_out) if type_out == 1 else ''
                    logging.info((
                        f'\tIN: ({name_in:>15},T={type_in:1},C={code_in:3},V={value_in:6}), '
                        f'\tOUT: ({name_out:>15},T={type_out:1},C={code_out:3},V={value_out:6})'))
                except KeyboardInterrupt:
                    kb.ungrab()
                    logging.error(traceback.format_exc())
                    sys.exit(0)
                
    except (PermissionError, ):
        logging.error("Must be run as sudo")

