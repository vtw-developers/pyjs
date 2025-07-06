def f_gold(s, t):
    count = 0
    for i in range(0, len(t)):
        if count == len(s):
            break
        if t[i] == s[count]:
            count = count + 1
    return count