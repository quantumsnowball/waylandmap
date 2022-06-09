import evdev


def get_devices() -> list:
    devices = [evdev.InputDevice(dev) for dev in evdev.list_devices()]
    return devices
