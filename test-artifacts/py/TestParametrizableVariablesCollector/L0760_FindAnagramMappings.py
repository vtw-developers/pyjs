mapper = defaultdict(set)
for i, num in enumerate(nums2):
    mapper[num].add(i)
return [mapper[num].pop() for num in nums1]