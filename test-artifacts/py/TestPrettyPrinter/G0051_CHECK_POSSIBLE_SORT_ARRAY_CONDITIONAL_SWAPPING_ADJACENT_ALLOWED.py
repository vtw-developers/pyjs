def f_gold(arr, n):
    for i in range(0, n - 1):
        if arr[i] > arr[i + 1]:
            if arr[i] - arr[i + 1] == 1:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
            else:
                return False
    return True