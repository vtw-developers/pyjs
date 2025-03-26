for i, c in enumerate(s):
    if c == ' ':
        k -= 1
    if k == 0:
        return s[:i]
return s