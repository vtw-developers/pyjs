'\n    :type s: string\n    :rtype int\n    '
Longest = temp = 0
stack = []
for i in s:
    if i == '(':
        stack.append(i)
    elif len(stack) != 0 and stack[-1] == '(':
        stack.pop()
        temp += 2
    else:
        stack = []
        if temp > Longest:
            Longest = temp
        temp = 0
if temp > Longest:
    Longest = temp
return Longest