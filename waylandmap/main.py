import click
from waylandmap.devices import get_devices
from waylandmap.keymapper import run


@click.command(short_help='WaylandMap is a keymapper tools that works on both X11 or Wayland machine.')
@click.option('-l', '--list-devices', is_flag=True, default=False, help='List name of all available devices. Please find you keyboard.')
@click.option('-n', '--name', default=None, help='Name of the target keyboard.')
@click.argument('keymaps', nargs=1, required=False, default=None)
def cli(list_devices, name, keymaps):
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
    if name is None:
        print('Please provide the name of you keyboard to remap. You may use the `-l` flag to show all available devices.')
        return
    else:
        devs = get_devices()
        for dev in devs:
            if name == dev.name:
                dev_path = dev.path
                break
        else:
            print('Name of devices does not exists. Please check your device name.')
            return
    if keymaps is None:
        print('Please provide the path to your keymap config file.')
        return
    # finally run the program
    run(dev_path, keymaps)

