import sys
import time
import evdev
import uinput
import logging
from waylandmap.filter import Filter
from waylandmap.constants import KEYS_VALUE_TUPLE, code_to_name
from waylandmap.devices import get_device_path


def infinite_retry(sleep, catch):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                except PermissionError:
                    logging.error("Must be run as sudo")
                except catch as e:
                    logging.error(f'{str(e)}: Failed to connect to device, possibly due to wake from sleep, will keep retrying ...')
                    time.sleep(sleep)
        return wrapped
    return wrapper


@infinite_retry(sleep=1, 
                catch=(FileNotFoundError, OSError, Exception))
def run(dev_name, keymaps):
    filter = Filter(keymaps)
    # start capturing from evdev
    kb = evdev.InputDevice(get_device_path(dev_name))
    kb.grab()

    try:
        with uinput.Device(KEYS_VALUE_TUPLE) as vdev:
            # loop to capture every event
            for ev in kb.read_loop():
                # each event represented by three ints
                type_in, code_in, value_in = ev.type, ev.code, ev.value
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
        logging.error('User keyboard interrupted, quitting now.')
        sys.exit(0)

