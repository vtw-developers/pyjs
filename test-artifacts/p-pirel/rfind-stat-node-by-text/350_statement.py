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
        break
    break