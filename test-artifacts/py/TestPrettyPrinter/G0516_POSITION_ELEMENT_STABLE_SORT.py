def f_gold(arr, n, idx):
    result = 0
    for i in range(n):
        if arr[i] < arr[idx]:
            result += 1
        if arr[i] == arr[idx] and i < idx:
            result += 1
    return result