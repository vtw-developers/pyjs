if x < y:
    return f_gold(s[::-1], y, x)
ans = 0
stk1, stk2 = ([], [])
for c in s:
    if c != 'b':
        stk1.append(c)
    elif stk1 and stk1[-1] == 'a':
        stk1.pop()
        ans += x
    else:
        stk1.append(c)
while stk1:
    c = stk1.pop()
    if c != 'b':
        stk2.append(c)
    elif stk2 and stk2[-1] == 'a':
        stk2.pop()
        ans += y
    else:
        stk2.append(c)
return ans