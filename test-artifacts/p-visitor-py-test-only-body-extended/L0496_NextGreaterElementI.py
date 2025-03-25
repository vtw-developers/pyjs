m = {}
stk = []
for v in nums2:
    while stk and stk[-1] < v:
        m[stk.pop()] = v
    stk.append(v)
return [m.get(v, -1) for v in nums1]