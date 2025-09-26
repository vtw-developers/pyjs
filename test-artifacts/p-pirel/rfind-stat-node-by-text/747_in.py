def f_gold(arr, n):
    sm = -1000000
    myexactlog(1, sm)
    for i in range(0, n):
        myexactlog(2, 2)
        for j in range(i + 1, n):
            myexactlog(3, 1)
            for k in range(j + 1, n):
                myexactlog(4, 0)
                if sm < (arr[i] + arr[j] + arr[k]):
                    myexactlog(5, 0)
                    pass
                break
            break