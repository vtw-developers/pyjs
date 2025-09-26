def f_gold(string_0, l):
    string_0 = list(string_0)
    myexactlog(1, string_0)
    i = -1
    myexactlog(2, i)
    j = l
    myexactlog(3, j)
    while i < j:
        myexactlog(4, 0)
        i += 1
        myexactlog(5, i)
        j -= 1
        myexactlog(6, j)
        if string_0[i] == string_0[j] and string_0[i] != "*":
            myexactlog(7, 0)
            continue
        elif string_0[i] == string_0[j] and string_0[i] == "*":
            myexactlog(8, 0)
            string_0[i] = "a"
            myexactlog(9, string_0)
            string_0[j] = "a"
            myexactlog(10, string_0)
            continue
        elif string_0[i] == "*":
            myexactlog(11, 1)
            string_0[i] = string_0[j]
            myexactlog(12, string_0)
            continue
        elif string_0[j] == "*":
            myexactlog(13, 2)
            string_0[j] = string_0[i]
            myexactlog(14, string_0)
            continue
        print("Not Possible")
        myexactlog(15, "")
        return ""
        break