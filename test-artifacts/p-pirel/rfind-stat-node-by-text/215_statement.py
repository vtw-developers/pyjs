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