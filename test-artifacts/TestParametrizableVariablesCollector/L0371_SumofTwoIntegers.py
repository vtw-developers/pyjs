a, b = (a & 4294967295, b & 4294967295)
while b:
    carry = (a & b) << 1 & 4294967295
    a, b = (a ^ b, carry)
return a if a < 2147483648 else ~(a ^ 4294967295)