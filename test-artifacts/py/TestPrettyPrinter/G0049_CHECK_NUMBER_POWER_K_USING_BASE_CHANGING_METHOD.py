def f_gold(n, k):
    oneSeen = False
    while n > 0:
        digit = n % k
        if digit > 1:
            return False
        if digit == 1:
            if oneSeen:
                return False
            oneSeen = True
        n //= k
    return True