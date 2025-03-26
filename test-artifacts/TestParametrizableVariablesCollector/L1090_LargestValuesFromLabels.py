arr = list(zip(values, labels))
arr.sort(reverse=True)
cnt = Counter()
ans = num = 0
for v, l in arr:
    if cnt[l] < useLimit:
        cnt[l] += 1
        num += 1
        ans += v
    if num == numWanted:
        break
return ans