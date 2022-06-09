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
        self._on_mods = {k[0]:False for k in self._combo}
        # self._mod_tree = { for c in self._combo}
        d = {}
        for c in self._combo:
            pth = []
            pth.append((c[1], c[2]))
            d[c] = pth

    def target(self, type_in: int, code_in: int, value_in: int) -> tuple | None:
        type_out, code_out, value_out = type_in, code_in, value_in
        # only interested in key event, ignore sync event
        if type_in == 1:
            # check if input is a modifier key
            if code_in in self._on_mods:
                # if confirm, change on_mods state
                self._on_mods[code_in] = value_in >= 1
                # then issue discard signal
                return None
            # check all registered mods tree and trigger
            for modifier, source, target in self._combo:
                # check if modifier is on
                if self._on_mods[modifier]:
                    # check if key pressed matched source
                    if code_in == source:
                        # change output target accordingly
                        code_out = target
                        # only need to match the first path
                        break
        # unless is a registered modifier key, always return a valid result
        return ((type_out, code_out), value_out)

