def f_gold(n):
    i = 0
    j = len(n)
    pos = 0
    while i < j:
        if n[i] == "4":
            pos = pos * 2 + 1
        if n[i] == "7":
            pos = pos * 2 + 2
        i = i + 1
    return pos