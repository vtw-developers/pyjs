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