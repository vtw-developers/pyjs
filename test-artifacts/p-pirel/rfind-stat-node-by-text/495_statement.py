for i in range(n):
    myexactlog(2, 2)
    left = 0
    myexactlog(3, left)
    right = 0
    myexactlog(4, right)
    for j in range(i - 1, -1, -1):
        myexactlog(5, 0)
        if templeHeight[j] < templeHeight[j + 1]:
            myexactlog(6, 0)
            left += 1
            myexactlog(7, left)
        else:
            myexactlog(8, 0)
            break
        break
    for j in range(i + 1, n):
        myexactlog(9, 1)
        if templeHeight[j] < templeHeight[j - 1]:
            myexactlog(10, 1)
            right += 1
            myexactlog(11, right)
        else:
            myexactlog(12, 1)
            break
        break
    sum_0 += max(right, left) + 1
    myexactlog(13, sum_0)
    break