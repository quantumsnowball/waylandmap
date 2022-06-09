import yaml


class Filter:
    def __init__(self, path: str):
        with open(path) as f:
            keymaps = yaml.safe_load(f)
        # organize into swap list and map list
        self._swap = tuple((m['target1'], m['target2'])
                           for m in keymaps if m['type'] == 'swap')
        self._map = tuple((m['source'], m['target'])
                          for m in keymaps if m['type'] == 'map')
        self._combo = tuple((m['modifier'], m['source'], m['target'])
                            for m in keymaps if m['type'] == 'combo')
        self._onMods = {k[0]:False for k in self._combo}


    def target(self, type: int, code: int, value: int) -> tuple:
        return ()

