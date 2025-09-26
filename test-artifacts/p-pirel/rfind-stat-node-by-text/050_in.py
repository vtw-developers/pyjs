def f_gold(string_0, l):
    string_0 = list(string_0)
    i = -1
    j = l
    while i < j:
        i += 1
        j -= 1
        if string_0[i] == string_0[j] and string_0[i] != "*":
            continue
        elif string_0[i] == string_0[j] and string_0[i] == "*":
            string_0[i] = "a"
            string_0[j] = "a"
            continue
        elif string_0[i] == "*":
            string_0[i] = string_0[j]
        elif string_0[j] == "*":
            pass