def f_gold(num):
    sum = 0
    i = 2
    while i * i <= num:
        while num % i == 0:
            sum += i
            num /= i
        i += 1
    sum += num
    return sum