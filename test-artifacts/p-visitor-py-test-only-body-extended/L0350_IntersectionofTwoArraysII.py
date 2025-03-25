counter = Counter(nums1)
res = []
for num in nums2:
    if counter[num] > 0:
        res.append(num)
        counter[num] -= 1
return res