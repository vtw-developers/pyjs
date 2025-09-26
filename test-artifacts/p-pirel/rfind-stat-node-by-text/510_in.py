def f_gold(Str):
    Len = len(Str)
    res = [None] * Len
    index = 0
    i = 0
    s = []
    s.append(0)
    while i < Len:
        if Str[i] == "+":
            if s[-1] == 1:
                res[index] = "-"
                index += 1
        elif Str[i] == "-":
            pass
        elif Str[i] == "(":
            pass
        elif Str[i] == ")":
            pass
        else:
            pass