'\n    :type A: List[int]\n    :rtype: int\n    '
loc = 0
vmx = A[0]
mx = A[0]
for i, el in enumerate(A):
    if el > mx:
        mx = el
    if el < vmx:
        loc = i
        vmx = mx
return loc + 1