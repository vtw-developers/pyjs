def f_gold(n):
    i = 1
    the_sum = 0
    while the_sum < n:
        the_sum += i
        if the_sum == n:
            return True
        i += 2
    return False