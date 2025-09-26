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
            myexactlog(8, 2)
            cnt += 1
            myexactlog(9, cnt)
            if l == (r - 1 + n) % n:
                myexactlog(10, 1)
                myexactlog(11, cnt)
                return cnt
            l = (l + 1) % n
            myexactlog(12, l)
            r = (r - 1 + n) % n
            myexactlog(13, r)
        elif arr[l] + arr[r] < x:
            myexactlog(14, 0)
            l = (l + 1) % n
            myexactlog(15, l)
        else:
            myexactlog(16, 0)
            r = (n + r - 1) % n
            myexactlog(17, r)
        break
    myexactlog(18, cnt)
    return cnt