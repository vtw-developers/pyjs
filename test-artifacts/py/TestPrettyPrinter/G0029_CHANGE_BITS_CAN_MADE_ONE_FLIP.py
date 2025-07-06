def f_gold(str):
    zeros = 0
    ones = 0
    for i in range(0, len(str)):
        ch = str[i]
        if ch == "0":
            zeros = zeros + 1
        else:
            ones = ones + 1
    return zeros == 1 or ones == 1