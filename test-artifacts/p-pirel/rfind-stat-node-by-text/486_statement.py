for i in range(n - 1, -1, -1):
    myexactlog(2, 3)
    for j in range(0, n):
        myexactlog(3, 2)
        if i == j:
            myexactlog(4, 0)
            continue
        for k in range(j + 1, n):
            myexactlog(5, 1)
            if i == k:
                myexactlog(6, 1)
                continue
            for l in range(k + 1, n):
                myexactlog(7, 0)
                if i == l:
                    myexactlog(8, 2)
                    continue
                if S[i] == S[j] + S[k] + S[l]:
                    myexactlog(9, 3)
                    retval_1 = S[i]
                    myexactlog(10, retval_1)
                    myexactlog(11, retval_1)
                    return retval_1
                break
            break
        break
    break