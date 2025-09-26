def f_gold(arr, n):
    vis = dict()
    myexactlog(1, vis)
    for i in range(n):
        myexactlog(2, 0)
        vis[arr[i]] = 1
        myexactlog(3, vis)
        break
    k = len(vis)
    myexactlog(4, k)
    vid = dict()
    myexactlog(5, vid)
    ans = 0
    myexactlog(6, ans)
    right = 0
    myexactlog(7, right)
    window = 0
    myexactlog(8, window)
    for left in range(n):
        myexactlog(9, 1)
        while right < n and window < k:
            myexactlog(10, 0)
            if arr[right] in vid.keys():
                myexactlog(11, 0)
                vid[arr[right]] += 1
                myexactlog(12, vid)
            else:
                myexactlog(13, 0)
                pass
            break