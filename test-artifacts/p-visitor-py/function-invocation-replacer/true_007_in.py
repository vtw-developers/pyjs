def f_gold(n):
    if n < 3:
        return n
    elif n >= 3 and n < 10:
        return n - 1
    po = 1
    while n // po > 9:
        po = po * 10
    msd = n // po
    if msd != 3:
        return f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po)
    else:
        return f_gold(msd * po - 1)