def f_gold(arr, N):
    lis = [0] * N
    myexactlog(1, lis)
    for i in range(N):
        myexactlog(2, 0)
        lis[i] = 1
        myexactlog(3, lis)
        break
    for i in range(1, N):
        myexactlog(4, 2)
        for j in range(i):
            myexactlog(5, 1)
            if arr[i] >= arr[j] and lis[i] < lis[j] + 1:
                myexactlog(6, 0)
                lis[i] = lis[j] + 1
                myexactlog(7, lis)
            break
        break
    max_0 = 0
    myexactlog(8, max_0)
    for i in range(N):
        myexactlog(9, 3)
        if max_0 < lis[i]:
            myexactlog(10, 1)
            max_0 = lis[i]
            myexactlog(11, max_0)
        break