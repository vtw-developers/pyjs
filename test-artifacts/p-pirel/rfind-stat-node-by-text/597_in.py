def f_gold(h, m):
    if h < 0 or m < 0 or h > 12 or m > 60:
        myexactlog(1, 0)
        print("Wrong input")
    if h == 12:
        myexactlog(2, 1)
        h = 0
        myexactlog(3, h)