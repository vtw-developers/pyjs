def f_gold(str):
    result = 0
    for i in range(len(str)):
        if (i == ord(str[i]) - ord("a")) or (i == ord(str[i]) - ord("A")):
            result += 1
    return result