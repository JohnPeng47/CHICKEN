# given val and dict returns key
def get_key_from_val(val, d):
    for key in d.keys():
        if d[key] == val:
            return key
    return None

