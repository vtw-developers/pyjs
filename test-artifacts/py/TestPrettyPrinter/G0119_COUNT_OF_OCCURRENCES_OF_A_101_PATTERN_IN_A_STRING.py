def f_gold(s):
    length = len(s)
    oneSeen = False
    count = 0
    for i in range(length):
        if s[i] == "1" and oneSeen:
            if s[i - 1] == "0":
                count += 1
        if s[i] == "1" and oneSeen == 0:
            oneSeen = True
        if s[i] != "0" and s[i] != "1":
            oneSeen = False
    return count