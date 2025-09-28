def f_gold(arr, n):
    if n == 1:
        myexactlog(1, 0)
        myexactlog(2, True)
        return True
    i = 1
    myexactlog(3, i)
    while i < n and arr[i - 1] < arr[i]:
        myexactlog(4, 0)
        i += 1
        myexactlog(5, i)
    if i == n:
        myexactlog(6, 1)
        myexactlog(7, True)
        return True
    j = i
    myexactlog(8, j)
    while j < n and arr[j] < arr[j - 1]:
        myexactlog(9, 1)
        if i > 1 and arr[j] < arr[i - 2]:
            myexactlog(10, 2)
            myexactlog(11, False)
            return False
        j += 1
        myexactlog(12, j)
    if j == n:
        myexactlog(13, 3)
        myexactlog(14, True)
        return True
    k = j
    myexactlog(15, k)