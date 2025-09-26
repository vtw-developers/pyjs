for j in range(len2 - 1, -1, -1):
    n2 = ord(num2[j]) - 48
    summ = n1 * n2 + result[i_n1 + i_n2] + carry
    carry = summ // 10
    result[i_n1 + i_n2] = summ % 10
    i_n2 += 1