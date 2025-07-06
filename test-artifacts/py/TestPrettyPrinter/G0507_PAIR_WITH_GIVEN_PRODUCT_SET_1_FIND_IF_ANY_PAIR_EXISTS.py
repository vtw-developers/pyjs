def f_gold(arr, n, x):
    for i in arr:
        for j in arr:
            if i * j == x:
                return True
    return False