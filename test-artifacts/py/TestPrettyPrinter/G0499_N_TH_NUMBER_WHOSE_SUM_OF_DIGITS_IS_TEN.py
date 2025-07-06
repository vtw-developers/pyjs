import itertools
def f_gold(n):
    count = 0
    for curr in itertools.count():
        sum = 0
        x = curr
        while x:
            sum = sum + x % 10
            x = x // 10
        if sum == 10:
            count = count + 1
        if count == n:
            return curr
    return -1