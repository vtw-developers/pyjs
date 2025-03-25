nums1.sort()
nums2.sort()
n, res = (len(nums1), 0)
for i in range(n):
    res += nums1[i] * nums2[n - i - 1]
return res