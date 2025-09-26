def f_gold(arr, n, x):
    i = 0
    myexactlog(1, i)
    for i in range(0, n - 1):
        myexactlog(2, 0)
        if arr[i] > arr[i + 1]:
            myexactlog(3, 0)
            break
        break
    l = (i + 1) % n
    myexactlog(4, l)
    r = i
    myexactlog(5, r)
    while l != r:
        myexactlog(6, 0)
        if arr[l] + arr[r] == x:
            myexactlog(7, 1)
            myexactlog(8, True)
            return True
        break