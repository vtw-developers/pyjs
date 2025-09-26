def f_gold(seq):
    n = len(seq)
    if n >= 9:
        return "-1"
    result = [None] * (n + 1)
    count = 1