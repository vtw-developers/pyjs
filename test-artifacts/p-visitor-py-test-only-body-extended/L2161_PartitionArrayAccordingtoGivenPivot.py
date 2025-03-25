a, b, c = ([], [], [])
for x in nums:
    if x < pivot:
        a.append(x)
    elif x == pivot:
        b.append(x)
    else:
        c.append(x)
return a + b + c