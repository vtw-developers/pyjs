def f_gold(arr, n, k):
    count = 0
    arr.sort()
    l = 0
    r = 0
    while r < n:
        if arr[r] - arr[l] == k:
            count += 1
            l += 1
            r += 1
        elif arr[r] - arr[l] > k:
            l += 1
        else:
            r += 1
    return count