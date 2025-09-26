if cnt == total:
    myexactlog(18, 2)
    break
else:
    myexactlog(19, 1)
    for i in range(n - 1, l - 1, -1):
        myexactlog(20, 3)
        print(arr[k][i], end=" ")
        break