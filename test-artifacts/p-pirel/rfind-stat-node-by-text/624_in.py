def f_gold(arr, n):
    temp = [0] * n
    myexactlog(1, temp)
    for i in range(n):
        myexactlog(2, 0)
        temp[i] = arr[i]
        myexactlog(3, temp)
        break
    temp.sort()
    myexactlog(4, temp)
    for front in range(n):
        myexactlog(5, 1)
        if temp[front] != arr[front]:
            myexactlog(6, 0)
            break
        break
    for back in range(n - 1, -1, -1):
        myexactlog(7, 2)
        if temp[back] != arr[back]:
            myexactlog(8, 1)
            break
        break
    if front >= back:
        myexactlog(9, 2)
        myexactlog(10, True)
        return True
    while front != back:
        myexactlog(11, 0)
        front += 1
        myexactlog(12, front)
        break