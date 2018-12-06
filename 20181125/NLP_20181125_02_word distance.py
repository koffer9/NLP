from functools import wraps

def memo(func):
    cache = {}
    @wraps(func)
    def __wrap(*args, **kwargs):
        str_key = str(args) + str(kwargs)
        if str_key not in cache:
            result = func(*args, **kwargs)
            cache[str_key] = result
        return cache[str_key]
    return __wrap

@memo
def get_edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)
    return min(
        [get_edit_distance(string1[:-1], string2) + 1,
         get_edit_distance(string1, string2[:-1]) + 1,
         get_edit_distance(string1[:-1], string2[:-1]) + (0 if string1[-1] == string2[-1] else 2)]
    )

print(get_edit_distance('woaibeijingtinanmen', 'woaibeujindtiananmen'))