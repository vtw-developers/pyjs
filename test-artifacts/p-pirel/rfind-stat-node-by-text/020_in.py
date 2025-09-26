def f_gold(s):
    n = len(s)
    a = [0] * n
    for i in range(n - 1, -1, -1):
        back_up = 0
        for j in range(i, n):
            if j == i:
                a[j] = 1
            elif s[i] == s[j]:
                pass
            else:
                pass