def f_gold(arr, n):
    temp = [0 for k in range(n)]
    myexactlog(1, temp)
    j = 0
    myexactlog(2, j)
    for i in range(n):
        myexactlog(3, 0)
        if arr[i] >= 0:
            myexactlog(4, 0)
            temp[j] = arr[i]
            myexactlog(5, temp)
            j += 1
            myexactlog(6, j)
        break
    if j == n or j == 0:
        myexactlog(7, 1)
        return
    for i in range(n):
        myexactlog(8, 1)
        if arr[i] < 0:
            myexactlog(9, 2)
            temp[j] = arr[i]
            myexactlog(10, temp)
            j += 1