def f_gold(str, corner):
    n = len(str)
    cl = len(corner)
    if n < cl:
        return False
    return (str[:cl] == corner) and (str[n - cl:] == corner)