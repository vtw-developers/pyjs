def f_gold(string):
    l = 0
    h = len(string) - 1
    while h > l:
        l += 1
        h -= 1
        if string[l - 1] != string[h + 1]:
            return False
    return True