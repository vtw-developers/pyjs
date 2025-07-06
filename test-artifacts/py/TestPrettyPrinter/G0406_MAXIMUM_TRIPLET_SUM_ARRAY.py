def f_gold(arr, n):
    sm = -1000000
    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if sm < (arr[i] + arr[j] + arr[k]):
                    sm = arr[i] + arr[j] + arr[k]
    return sm