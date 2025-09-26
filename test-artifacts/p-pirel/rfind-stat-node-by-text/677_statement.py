for i in range(n):
    s[arr[i]] = 1
    if arr[i] < minm:
        minm = arr[i]
    if arr[i] > maxm:
        maxm = arr[i]