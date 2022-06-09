# WaylandMap

I started to code this program because I want to use RightAlt + hjkl as system-wide arrow keys. Everyone has been using `xmodmap` to remap keys on linux. However, after switching to Wayland window system, `xmodmap` stopped working. I started to look for ready-to-use solution but with no luck. Probably Wayland are still too new for the community to catch up. Luckly, Google gave me some hints on how to achieve this task. The key is to go to lower level! This module makes use of `evdev` and `uinput` module to achieve keymapping. Therefore it should work on any Desktop, such as X11 or Wayland.

## Install
Simply install using `pip` and run it as a cli application:
```
pip install waylandmap
```
It is recommended to install the package to its own virtual environment, especially when installed as a linux system service. For example, install using `pipx`:
```
pipx install waylandmap
```

## Usage
Your can run the keymapper directly by supplying the name of keyboard and the keymap file.
```bash
sudo waylandmap -n <name-of-your-keyboard> <path/to/config.yml>
```
You can see the key event inputs and outputs printed out in real time by running in debug mode. You can also check the string name required by the config file.
```bash
sudo waylandmap --debug -n <name-of-your-keyboard> <path/to/config.yml>
```

## Configuration
The program accept a config file path as argument. The config file should be in yaml format.
```yaml
# keymaps.yaml

# # RightAlt + hjkl to arrows
- type: combo 
  modifier: KEY_RIGHTALT
  source: KEY_H
  target: KEY_LEFT
- type: combo 
  modifier: KEY_RIGHTALT
  source: KEY_J
  target: KEY_DOWN
- type: combo 
  modifier: KEY_RIGHTALT
  source: KEY_K
  target: KEY_UP
- type: combo 
  modifier: KEY_RIGHTALT
  source: KEY_L
  target: KEY_RIGHT

```

## Install as Linux system services

After writing your config file and test running it without problem, your can install the program as a system services. This should w automatically start the keymapper when you login.

```
TODO
```
