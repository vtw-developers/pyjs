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