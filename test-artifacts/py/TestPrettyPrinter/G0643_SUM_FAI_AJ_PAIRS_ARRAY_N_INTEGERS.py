def f_gold(a, n):
    cnt = dict()
    ans = 0
    pre_sum = 0
    for i in range(n):
        ans += (i * a[i]) - pre_sum
        pre_sum += a[i]
        if (a[i] - 1) in cnt:
            ans -= cnt[a[i] - 1]
        if (a[i] + 1) in cnt:
            ans += cnt[a[i] + 1]
        if a[i] not in cnt:
            cnt[a[i]] = 0
        cnt[a[i]] += 1
    return ans