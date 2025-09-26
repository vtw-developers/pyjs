def f_gold(arr, n):
    difference = 0
    myexactlog(1, difference)
    ans = 0
    myexactlog(2, ans)
    hash_positive = [0] * (n + 1)
    myexactlog(3, hash_positive)
    hash_negative = [0] * (n + 1)
    myexactlog(4, hash_negative)
    hash_positive[0] = 1
    myexactlog(5, hash_positive)
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
            ans += hash_positive[difference]
            myexactlog(15, ans)