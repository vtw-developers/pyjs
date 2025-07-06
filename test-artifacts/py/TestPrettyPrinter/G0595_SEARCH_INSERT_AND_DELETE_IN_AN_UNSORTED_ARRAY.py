def f_gold(arr, n, key):
    for i in range(n):
        if arr[i] == key:
            return i
    return -1