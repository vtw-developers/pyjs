def f_gold(str):
    n = len(str)
    res = -1
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            if str[i] == str[j]:
                res = max(res, abs(j - i - 1))
    return res