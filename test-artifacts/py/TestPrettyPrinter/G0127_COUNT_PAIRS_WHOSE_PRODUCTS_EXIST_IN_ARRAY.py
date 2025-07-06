def f_gold(arr, n):
    result = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            product = arr[i] * arr[j]
            for k in range(0, n):
                if arr[k] == product:
                    result = result + 1
                    break
    return result