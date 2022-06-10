from evdev.ecodes import EV_KEY
import yaml
from waylandmap.constants import name_to_code as ntc


class Filter:
    def __init__(self, path: str):
        with open(path) as f:
            keymaps = yaml.safe_load(f)
        # organize into swap list and map list
        self._swap = tuple((ntc(m['target1']), ntc(m['target2']))
                           for m in keymaps if m['type'] == 'swap')
        self._map = tuple((ntc(m['source']), ntc(m['target']))
                          for m in keymaps if m['type'] == 'map')
        self._combo = tuple((ntc(m['modifier']), ntc(m['source']), ntc(m['target']))
                            for m in keymaps if m['type'] == 'combo')
        # modifier keys states
        self._on_modifier = {k[0]:False for k in self._combo}
        # mapping path states
        self._on_combo = {c:False for c in self._combo}

    def target(self, type_in: int, code_in: int, value_in: int) -> tuple | None:
        type_out, code_out, value_out = type_in, code_in, value_in
        # only interested in key event, ignore sync event
        if type_in == EV_KEY:
            # check if input is a modifier key
            if code_in in self._on_modifier:
                # if confirm, change on_mods state
                self._on_modifier[code_in] = value_in >= 1
                # then issue discard signal
                return None
            # check all registered mods tree and trigger
            for remap_path in self._combo:
                modifier, source, target = remap_path
                # check if modifier is on, or on_mapping flag is on
                if self._on_modifier[modifier] or self._on_combo[remap_path]:
                    # check if key pressed matched source
                    if code_in == source:
                        # change output target accordingly
                        code_out = target
                        # mark remap path flag to on, only turn off upon key release event
                        self._on_combo[remap_path] = value_in >= 1
                        # only need to match the first path
                        break
        # unless is a registered modifier key, always return a valid result
        return ((type_out, code_out), value_out)

