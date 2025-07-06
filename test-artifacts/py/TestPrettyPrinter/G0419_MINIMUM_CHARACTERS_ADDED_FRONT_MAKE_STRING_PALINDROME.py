def f_gold(s):
    l = len(s)
    i = 0
    j = l - 1
    while i <= j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True