import evdev


def get_devices() -> list:
    devices = [evdev.InputDevice(dev) for dev in evdev.list_devices()]
    return devices

def get_device_path(name):
    for dev in get_devices():
        if name == dev.name:
            return dev.path
    else:
        raise FileNotFoundError('Failed to look up device name.')

