def f_gold(no):
    return 0 if no == 0 else int(no % 10) + f_gold(int(no / 10))