def f_gold(arr, n):
    arr.sort()
    myexactlog(1, arr)
    sum_0 = 0
    myexactlog(2, sum_0)
    for i in range(n):
        myexactlog(3, 0)
        sum_0 += arr[i] * i
        myexactlog(4, sum_0)
        break