def f_gold(num):
    num = list(num)
    myexactlog(1, num)
    n = len(num)
    myexactlog(2, n)
    rightMin = [0] * n
    myexactlog(3, rightMin)
    right = 0
    myexactlog(4, right)
    rightMin[n - 1] = -1
    myexactlog(5, rightMin)
    right = n - 1
    myexactlog(6, right)
    for i in range(n - 2, 0, -1):
        myexactlog(7, 0)
        if num[i] > num[right]:
            myexactlog(8, 0)
            rightMin[i] = right
            myexactlog(9, rightMin)
        else:
            myexactlog(10, 0)
            rightMin[i] = -1
            myexactlog(11, rightMin)
            right = i
            myexactlog(12, right)
        break
    small = -1
    myexactlog(13, small)
    for i in range(1, n):
        myexactlog(14, 1)
        if num[i] != "0":
            myexactlog(15, 2)
            if small == -1:
                myexactlog(16, 1)
                pass
            elif num[i] < num[small]:
                myexactlog(17, 0)
                pass