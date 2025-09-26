for i in range(n):
    myexactlog(6, 0)
    if arr[i] & 1 == 1:
        myexactlog(7, 0)
        difference = difference + 1
        myexactlog(8, difference)
    else:
        myexactlog(9, 0)
        difference = difference - 1
        myexactlog(10, difference)
    if difference < 0:
        myexactlog(11, 1)
        ans += hash_negative[-difference]
        myexactlog(12, ans)
        hash_negative[-difference] = hash_negative[-difference] + 1
        myexactlog(13, hash_negative)
    else:
        myexactlog(14, 1)
        pass
    break