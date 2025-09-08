def f_gold(a, n):
    count = dict()
    for i in range(n):
        if count.get(a[i]):
            count[a[i]] += 1
        else:
            count[a[i]] = 1
    next_missing = 1
    for i in range(n):
        if count[a[i]] != 1 or a[i] > n or a[i] < 1:
            count[a[i]] -= 1
            while count.get(next_missing):
                next_missing += 1
            a[i] = next_missing
            count[next_missing] = 1