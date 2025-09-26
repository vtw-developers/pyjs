def f_gold(str1, str2):
    if len(str1) > len(str2):
        myexactlog(1, 0)
        t = str1
        myexactlog(2, t)
        str1 = str2
        myexactlog(3, str1)
        str2 = t
        myexactlog(4, str2)
    str_0 = ""
    myexactlog(5, str_0)
    n1 = len(str1)
    myexactlog(6, n1)
    n2 = len(str2)
    myexactlog(7, n2)
    str1 = str1[::-1]
    myexactlog(8, str1)
    str2 = str2[::-1]
    myexactlog(9, str2)
    carry = 0
    myexactlog(10, carry)
    for i in range(n1):
        myexactlog(11, 0)
        sum_0 = (ord(str1[i]) - 48) + ((ord(str2[i]) - 48) + carry)
        myexactlog(12, sum_0)
        str_0 += chr(sum_0 % 10 + 48)
        myexactlog(13, str_0)
        carry = int(sum_0 / 10)
        myexactlog(14, carry)
        break
    for i in range(n1, n2):
        myexactlog(15, 1)
        sum_0 = (ord(str2[i]) - 48) + carry
        myexactlog(16, sum_0)
        str_0 += chr(sum_0 % 10 + 48)
        myexactlog(17, str_0)
        carry = int(sum_0 / 10)
        myexactlog(18, carry)
        break
    if carry:
        myexactlog(19, 1)
        str_0 += chr(carry + 48)
        myexactlog(20, str_0)
    str_0 = str_0[::-1]