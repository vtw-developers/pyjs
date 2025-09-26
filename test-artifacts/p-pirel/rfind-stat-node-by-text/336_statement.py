for j in range(m):
    myexactlog(6, 1)
    if arr1[i] == arr2[j]:
        myexactlog(7, 1)
        if current + 1 > table[j]:
            myexactlog(8, 0)
            table[j] = current + 1
            myexactlog(9, table)
    if arr1[i] > arr2[j]:
        myexactlog(10, 3)
        if table[j] > current:
            myexactlog(11, 2)
            current = table[j]
            myexactlog(12, current)
    break