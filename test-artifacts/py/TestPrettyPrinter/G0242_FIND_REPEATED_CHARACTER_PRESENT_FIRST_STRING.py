def f_gold(s):
    p = -1
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] == s[j]:
                p = i
                break
        if p != -1:
            break
    return p