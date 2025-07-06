def f_gold(arr, n, m):
    max = 0
    min = 0
    arr.sort()
    j = n - 1
    for i in range(m):
        min += arr[i]
        max += arr[j]
        j = j - 1
    return max - min