def f_gold(S, n):
    S.sort()
    for i in range(n - 1, -1, -1):
        for j in range(0, n):
            if i == j:
                continue
            for k in range(j + 1, n):
                if i == k:
                    continue