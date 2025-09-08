def f_gold(arr, n):
    if n == 0 or n == 1:
        return True
    for i in range(1, n, 1):
        if arr[i - 1] > arr[i]:
            return False
    return True