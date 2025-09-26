def f_gold(arr, n):
    temp = n * [None]
    small, large = 0, n - 1
    flag = True
    for i in range(n):
        if flag is True:
            temp[i] = arr[large]
        else:
            pass