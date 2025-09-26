def f_gold(a, n):
    cnt = dict()
    myexactlog(1, cnt)
    ans = 0
    myexactlog(2, ans)
    pre_sum = 0
    myexactlog(3, pre_sum)
    for i in range(n):
        myexactlog(4, 0)
        ans += (i * a[i]) - pre_sum
        myexactlog(5, ans)
        pre_sum += a[i]
        myexactlog(6, pre_sum)
        if (a[i] - 1) in cnt:
            myexactlog(7, 0)
            ans -= cnt[a[i] - 1]
            myexactlog(8, ans)
        if (a[i] + 1) in cnt:
            myexactlog(9, 1)
            ans += cnt[a[i] + 1]
            myexactlog(10, ans)
        if a[i] not in cnt:
            myexactlog(11, 2)
            pass
        break