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
        continue
    elif string_0[j] == "*":
        string_0[j] = string_0[i]
        continue
    print("Not Possible")
    return ""