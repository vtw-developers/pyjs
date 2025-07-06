def f_gold(s, t, n, k):
    last = 0
    cnt = 0
    new_last = 0
    size = 0
    string = "zyxwvutsrqponmlkjihgfedcba"
    for ch in string:
        cnt = 0
        for i in range(last, n):
            if s[i] == ch:
                cnt += 1
        if cnt >= k:
            for i in range(last, n):
                if s[i] == ch:
                    t[size] = ch
                    new_last = i
                    size += 1
            last = new_last