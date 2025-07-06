def f_gold(a, b):
    s = str(b)
    i = 0
    while i < (len(s)):
        if s[i] != "9":
            break
        i += 1
    result = 0
    if i == len(s):
        result = a * len(s)
    else:
        result = a * (len(s) - 1)
    return result