def f_gold(num):
    length = len(num)
    if length == 1 and num[0] == "0":
        return True
    if length % 3 == 1:
        num = str(num) + "00"
        length += 2
    elif length % 3 == 2:
        num = str(num) + "0"
        length += 1
    sum = 0
    p = 1
    for i in range(length - 1, -1, -1):
        group = 0
        group += ord(num[i]) - ord("0")
        i -= 1
        group += (ord(num[i]) - ord("0")) * 10
        i -= 1
        group += (ord(num[i]) - ord("0")) * 100
        sum = sum + group * p
        p *= -1
    sum = abs(sum)
    return sum % 13 == 0