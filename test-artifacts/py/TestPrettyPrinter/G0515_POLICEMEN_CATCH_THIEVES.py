def f_gold(arr, n, k):
    i = 0
    l = 0
    r = 0
    res = 0
    thi = []
    pol = []
    while i < n:
        if arr[i] == "P":
            pol.append(i)
        elif arr[i] == "T":
            thi.append(i)
        i += 1
    while l < len(thi) and r < len(pol):
        if abs(thi[l] - pol[r]) <= k:
            res += 1
            l += 1
            r += 1
        elif thi[l] < pol[r]:
            l += 1
        else:
            r += 1
    return res