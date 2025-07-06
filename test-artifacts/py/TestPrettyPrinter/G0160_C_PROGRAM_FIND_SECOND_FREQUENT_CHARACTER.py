def f_gold(str):
    NO_OF_CHARS = 256
    count = [0] * NO_OF_CHARS
    for i in range(len(str)):
        count[ord(str[i])] += 1
    first, second = 0, 0
    for i in range(NO_OF_CHARS):
        if count[i] > count[first]:
            second = first
            first = i
        elif count[i] > count[second] and count[i] != count[first]:
            second = i
    return chr(second)