stk = []
for c in s:
    if c == '(':
        stk.append(c)
    elif stk and stk[-1] == '(':
        stk.pop()
    else:
        stk.append(c)
return len(stk)