ans = []
j = 0
for i, c in enumerate(s):
    if j < len(spaces) and i == spaces[j]:
        ans.append(' ')
        j += 1
    ans.append(c)
return ''.join(ans)