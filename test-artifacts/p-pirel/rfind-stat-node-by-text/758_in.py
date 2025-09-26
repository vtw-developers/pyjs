def f_gold(arr, n, x):
    i = 0
    myexactlog(1, i)
    for i in range(n):
        myexactlog(2, 0)
        if arr[i] > arr[i + 1]:
            myexactlog(3, 0)
            break
        break
    l = (i + 1) % n
    myexactlog(4, l)
    r = i
    myexactlog(5, r)
    cnt = 0
    myexactlog(6, cnt)
    while l != r:
        myexactlog(7, 0)
        if arr[l] + arr[r] == x:
            myexactlog(8, 1)
            pass
        elif arr[l] + arr[r] < x:
            myexactlog(9, 0)
            pass
        else:
            myexactlog(10, 0)
            pass