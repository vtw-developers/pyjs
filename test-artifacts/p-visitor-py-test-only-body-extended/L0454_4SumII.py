counter = Counter()
for a in nums1:
    for b in nums2:
        counter[a + b] += 1
ans = 0
for c in nums3:
    for d in nums4:
        ans += counter[-(c + d)]
return ans