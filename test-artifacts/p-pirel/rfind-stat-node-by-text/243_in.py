def f_gold(arr, n):
    difference = 0
    ans = 0
    hash_positive = [0] * (n + 1)
    hash_negative = [0] * (n + 1)
    hash_positive[0] = 1
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