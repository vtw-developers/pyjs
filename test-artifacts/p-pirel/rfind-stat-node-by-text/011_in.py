def f_gold(arr, n):
    inc, dcr = dict(), dict()
    len_inc, len_dcr = [0] * n, [0] * n
    longLen = 0
    for i in range(n):
        len_0 = 0
        if inc.get(arr[i] - 1) in inc.values():
            len_0 = inc.get(arr[i] - 1)
        inc[arr[i]] = len_inc[i] = len_0 + 1
    for i in range(n - 1, -1, -1):
        len_0 = 0