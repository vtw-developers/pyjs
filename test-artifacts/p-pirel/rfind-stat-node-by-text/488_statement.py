while i < Len:
    if Str[i] == "+":
        if s[-1] == 1:
            res[index] = "-"
            index += 1
        if s[-1] == 0:
            res[index] = "+"
            index += 1
    elif Str[i] == "-":
        if s[-1] == 1:
            res[index] = "+"
            index += 1
        if s[-1] == 0:
            res[index] = "-"
            index += 1
    elif Str[i] == "(":
        if Str[i - 1] == "-" and i > 0:
            x = 0 if (s[-1] == 1) else 1
            s.append(x)
        elif Str[i - 1] == "+":
            s.append(s[-1])
    elif Str[i] == ")":
        s.pop()
    else:
        res[index] = Str[i]
        index += 1
    i += 1