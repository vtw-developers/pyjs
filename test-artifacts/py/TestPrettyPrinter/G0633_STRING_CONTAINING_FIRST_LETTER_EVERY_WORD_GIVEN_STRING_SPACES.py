def f_gold(str):
    result = ""
    v = True
    for i in range(len(str)):
        if str[i] == " ":
            v = True
        elif str[i] != " " and v == True:
            result += str[i]
            v = False
    return result