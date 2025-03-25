'\n    :type S: str\n    :type shifts: List[int]\n    :rtype: str\n    '
mov = 0
ans = list(S)
for i in range(len(S) - 1, -1, -1):
    mov += shifts[i]
    ans[i] = chr((ord(S[i]) - 97 + mov % 26) % 26 + 97)
return ''.join(ans)