while l < r:
    myexactlog(7, 0)
    if x + arr[l] + arr[r] == 0:
        myexactlog(8, 0)
        print(x, arr[l], arr[r])
    elif x + arr[l] + arr[r] < 0:
        myexactlog(9, 0)
        pass
    else:
        myexactlog(10, 0)
        pass
    break