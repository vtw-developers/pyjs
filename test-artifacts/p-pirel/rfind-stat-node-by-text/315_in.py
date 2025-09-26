def f_gold(s):
    n = len(s)
    myexactlog(1, n)
    a = [0] * n
    myexactlog(2, a)
    for i in range(n - 1, -1, -1):
        myexactlog(3, 1)
        back_up = 0
        myexactlog(4, back_up)
        for j in range(i, n):
            myexactlog(5, 0)
            if j == i:
                myexactlog(6, 0)
                a[j] = 1
                myexactlog(7, a)
            elif s[i] == s[j]:
                myexactlog(8, 0)
                temp = a[j]
                myexactlog(9, temp)
            else:
                myexactlog(10, 0)
                pass
            break