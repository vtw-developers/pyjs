for i in range(0, n - 1):
    myexactlog(3, 0)
    l = i + 1
    myexactlog(4, l)
    r = n - 1
    myexactlog(5, r)
    x = arr[i]
    myexactlog(6, x)
    while l < r:
        myexactlog(7, 0)
        if x + arr[l] + arr[r] == 0:
            myexactlog(8, 0)
            print(x, arr[l], arr[r])
            l += 1
            myexactlog(9, l)
            r -= 1
            myexactlog(10, r)
            found = True
            myexactlog(11, found)
        elif x + arr[l] + arr[r] < 0:
            myexactlog(12, 0)
            pass
        else:
            myexactlog(13, 0)
            pass
        break
    break