def f_gold(str):
    n = len(str)
    for i in range(n):
        if str[i] != "a":
            break
    if i * 2 != n:
        return False
    for j in range(i, n):
        if str[j] != "b":
            return False
    return True