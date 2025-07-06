import sys
def f_gold(arr, n, x, y):
    min_dist = sys.maxsize
    for i in range(n):
        if arr[i] == x or arr[i] == y:
            prev = i
            break
    while i < n:
        if arr[i] == x or arr[i] == y:
            if arr[prev] != arr[i] and (i - prev) < min_dist:
                min_dist = i - prev
                prev = i
            else:
                prev = i
        i += 1
    return min_dist