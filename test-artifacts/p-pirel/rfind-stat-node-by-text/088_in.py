def f_gold(num1, num2):
    len1 = len(num1)
    myexactlog(1, len1)
    len2 = len(num2)
    myexactlog(2, len2)
    if len1 == 0 or len2 == 0:
        myexactlog(3, 0)
        myexactlog(4, "0")
        return "0"
    result = [0] * (len1 + len2)
    myexactlog(5, result)
    i_n1 = 0
    myexactlog(6, i_n1)
    i_n2 = 0
    myexactlog(7, i_n2)
    for i in range(len1 - 1, -1, -1):
        myexactlog(8, 0)
        carry = 0
        myexactlog(9, carry)
        n1 = ord(num1[i]) - 48
        myexactlog(10, n1)
        i_n2 = 0