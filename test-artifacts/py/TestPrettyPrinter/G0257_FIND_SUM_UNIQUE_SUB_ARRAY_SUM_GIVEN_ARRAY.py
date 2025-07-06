def f_gold(arr, n):
    res = 0
    m = dict()
    for i in range(n):
        Sum = 0
        for j in range(i, n):
            Sum += arr[j]
            m[Sum] = m.get(Sum, 0) + 1
    for x in m:
        if m[x] == 1:
            res += x
    return res