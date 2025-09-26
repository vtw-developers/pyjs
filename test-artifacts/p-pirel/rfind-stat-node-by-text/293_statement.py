for i in range(len1 - 1, -1, -1):
    carry = 0
    n1 = ord(num1[i]) - 48
    i_n2 = 0
    for j in range(len2 - 1, -1, -1):
        n2 = ord(num2[j]) - 48
        summ = n1 * n2 + result[i_n1 + i_n2] + carry
        carry = summ // 10
        result[i_n1 + i_n2] = summ % 10
        i_n2 += 1
    if carry > 0:
        result[i_n1 + i_n2] += carry
    i_n1 += 1