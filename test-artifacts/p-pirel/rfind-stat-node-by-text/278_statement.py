for j in range(i + 1, n):
    myexactlog(7, 2)
    abs_diff = abs(arr[i] - arr[j])
    myexactlog(8, abs_diff)
    if abs_diff in mp.keys():
        myexactlog(9, 1)
        p = mp[abs_diff]
        myexactlog(10, p)
        if p[0] != i and p[0] != j and p[1] != i and p[1] != j:
            myexactlog(11, 0)
            pass
    break