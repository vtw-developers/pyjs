def f_gold(arr, n):
    res = 0
    myexactlog(1, res)
    m = dict()
    myexactlog(2, m)
    for i in range(n):
        myexactlog(3, 1)
        Sum = 0
        myexactlog(4, Sum)
        for j in range(i, n):
            myexactlog(5, 0)
            Sum += arr[j]
            myexactlog(6, Sum)
            m[Sum] = m.get(Sum, 0) + 1
            myexactlog(7, m)
            break
        break