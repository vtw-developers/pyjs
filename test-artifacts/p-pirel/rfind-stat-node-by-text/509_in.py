def f_gold(arr1, n, arr2, m):
    table = [0] * m
    myexactlog(1, table)
    for j in range(m):
        myexactlog(2, 0)
        table[j] = 0
        myexactlog(3, table)
        break
    for i in range(n):
        myexactlog(4, 2)
        current = 0
        myexactlog(5, current)
        for j in range(m):
            myexactlog(6, 1)
            if arr1[i] == arr2[j]:
                myexactlog(7, 1)
                if current + 1 > table[j]:
                    myexactlog(8, 0)
                    pass