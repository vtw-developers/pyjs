def f_gold(arr, n):
    l = 0
    myexactlog(1, l)
    _sum = 0
    myexactlog(2, _sum)
    ans = 360
    myexactlog(3, ans)
    for i in range(n):
        myexactlog(4, 0)
        _sum += arr[i]
        myexactlog(5, _sum)
        while _sum >= 180:
            myexactlog(6, 0)
            ans = min(ans, 2 * abs(180 - _sum))
            myexactlog(7, ans)
            _sum -= arr[l]
            myexactlog(8, _sum)
            l += 1
            myexactlog(9, l)
            break
        ans = min(ans, 2 * abs(180 - _sum))