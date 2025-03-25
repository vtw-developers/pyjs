stk = []
for s in path.split('/'):
    if not s or s == '.':
        continue
    if s == '..':
        if stk:
            stk.pop()
    else:
        stk.append(s)
return '/' + '/'.join(stk)