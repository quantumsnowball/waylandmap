import click
import logging
from waylandmap.devices import get_devices
from waylandmap.keymapper import run


@click.command(short_help='WaylandMap is a keymapper tools that works on both X11 or Wayland machine.')
@click.option('-l', '--list-devices', is_flag=True, default=False, help='List name of all available devices. Please find you keyboard.')
@click.option('-n', '--name', default=None, help='Name of the target keyboard.')
@click.argument('keymaps', nargs=1, required=False, default=None)
@click.option('-v', '--verbose', is_flag=True, default=False, help='Print live event mapping info to terminal.')
def cli(list_devices, name, keymaps, verbose):
    """KEYMAPS is the path to your config yaml file"""
    # show available devices
    if list_devices:
        devs = get_devices()
        if len(devs) == 0:
            click.echo('Need root permission to access devices.')
        else:
            print('List of avaliable devices:')
            for dev in devs:
                print(f'{dev.path}\t\t{dev.name}')
        return
    # ensure device name
    if name is None:
        print('Please provide the name of you keyboard to remap. You may use the `-l` flag to show all available devices.')
        return
    else:
        devs = get_devices()
        for dev in devs:
            if name == dev.name:
                dev_name = dev.name
                break
        else:
            print('Name of devices does not exists. Please check your device name.')
            return
    # ensure keymap config file
    if keymaps is None:
        print('Please provide the path to your keymap config file.')
        return
    # set log level
    logging.basicConfig(format='%(message)s',
                        level=logging.DEBUG if verbose else logging.WARNING)
    # finally run the program
    run(dev_name, keymaps)

