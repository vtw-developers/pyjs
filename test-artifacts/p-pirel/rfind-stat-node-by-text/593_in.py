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
        myexactlog(8, 1)
        carry = 0
        myexactlog(9, carry)
        n1 = ord(num1[i]) - 48
        myexactlog(10, n1)
        i_n2 = 0
        myexactlog(11, i_n2)
        for j in range(len2 - 1, -1, -1):
            myexactlog(12, 0)
            n2 = ord(num2[j]) - 48
            myexactlog(13, n2)
            summ = n1 * n2 + result[i_n1 + i_n2] + carry
            myexactlog(14, summ)
            carry = summ // 10
            myexactlog(15, carry)
            result[i_n1 + i_n2] = summ % 10
            myexactlog(16, result)
            i_n2 += 1
            myexactlog(17, i_n2)
            break
        if carry > 0:
            myexactlog(18, 1)
            result[i_n1 + i_n2] += carry
            myexactlog(19, result)
        i_n1 += 1
        myexactlog(20, i_n1)
        break
    i = len(result) - 1
    myexactlog(21, i)
    while i >= 0 and result[i] == 0:
        myexactlog(22, 0)
        i -= 1
        myexactlog(23, i)
        break
    if i == -1:
        myexactlog(24, 2)
        myexactlog(25, "0")
        return "0"