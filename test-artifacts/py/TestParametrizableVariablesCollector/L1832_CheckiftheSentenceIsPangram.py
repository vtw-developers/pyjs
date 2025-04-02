res = 0
for c in sentence:
    res |= 1 << ord(c) - ord('a')
    if res == 67108863:
        return True
return False