for i in range(n):
    if arr[i] & 1 == 1:
        difference = difference + 1
    else:
        difference = difference - 1
    if difference < 0:
        ans += hash_negative[-difference]
        hash_negative[-difference] = hash_negative[-difference] + 1
    else:
        ans += hash_positive[difference]
        hash_positive[difference] = hash_positive[difference] + 1