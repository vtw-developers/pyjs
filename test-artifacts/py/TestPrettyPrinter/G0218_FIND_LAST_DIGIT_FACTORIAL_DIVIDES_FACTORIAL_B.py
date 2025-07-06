def f_gold(A, B):
    variable = 1
    if A == B:
        return 1
    elif (B - A) >= 5:
        return 0
    else:
        for i in range(A + 1, B + 1):
            variable = (variable * (i % 10)) % 10
        return variable % 10