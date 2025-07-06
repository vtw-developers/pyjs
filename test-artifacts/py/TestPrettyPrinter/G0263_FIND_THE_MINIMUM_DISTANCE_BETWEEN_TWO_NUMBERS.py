def f_gold(arr, n, x, y):
    min_dist = 99999999
    for i in range(n):
        for j in range(i + 1, n):
            if (x == arr[i] and y == arr[j] or y == arr[i] and x == arr[j]) and min_dist > abs(i - j):
                min_dist = abs(i - j)
        return min_dist