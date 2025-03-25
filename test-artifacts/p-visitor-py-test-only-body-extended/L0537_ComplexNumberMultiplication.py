a, b = map(int, num1[:-1].split('+'))
c, d = map(int, num2[:-1].split('+'))
return f'{a * c - b * d}+{a * d + c * b}i'