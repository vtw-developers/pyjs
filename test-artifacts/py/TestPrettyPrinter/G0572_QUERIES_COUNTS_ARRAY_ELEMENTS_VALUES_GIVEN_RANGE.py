def f_gold(arr, n, x, y):
    count = 0
    for i in range(n):
        if arr[i] >= x and arr[i] <= y:
            count += 1
    return count