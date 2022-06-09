import uinput

# {'ITEM_XXX': (0,0)}
EVENTS_NAME_VALUE_DICT = {
    k:v for k,v in vars(uinput.ev).items()
    if k.startswith(('KEY_', 'BTN_', 'REL_', 'ABS_', ))}

# {'KEY_XXX': (0,0)}
KEYS_NAME_VALUE_DICT = {
    k:v for k,v in EVENTS_NAME_VALUE_DICT.items()
    if k.startswith('KEY_')}

# {(0,0), ...}
KEYS_VALUE_TUPLE = KEYS_NAME_VALUE_DICT.values()

# {(0,0): 'KEY_XXX'}
KEYS_VALUE_NAME_DICT = {
    v:k for k,v in KEYS_NAME_VALUE_DICT.items()}

# {'KEY_XXX': 0}
KEY_NAME_CODE_DICT = {
    k:v[1] for k,v in KEYS_NAME_VALUE_DICT.items()}

# {0: 'KEY_XXX'}
KEY_CODE_NAME_DICT = {
    v:k for k,v in KEY_NAME_CODE_DICT.items()}

def name_to_code(name: str) -> int:
    code = KEY_NAME_CODE_DICT[name]
    return code

def code_to_name(code: int) -> str:
    name = KEY_CODE_NAME_DICT[code]
    return name
