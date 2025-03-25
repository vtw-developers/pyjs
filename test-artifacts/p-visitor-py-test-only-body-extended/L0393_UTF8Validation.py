n = 0
for v in data:
    if n > 0:
        if v >> 6 != 2:
            return False
        n -= 1
    elif v >> 7 == 0:
        n = 0
    elif v >> 5 == 6:
        n = 1
    elif v >> 4 == 14:
        n = 2
    elif v >> 3 == 30:
        n = 3
    else:
        return False
return n == 0