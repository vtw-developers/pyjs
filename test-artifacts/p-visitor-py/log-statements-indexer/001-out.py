def test():
    f_gold()
"-----------------"
def f_gold():
    n = 0
    myexactlog(1, n)
    print(n)
    n = 1
    myexactlog(2, n)
    while n < 10:
        myexactlog(3, 0)
        n += 1
        myexactlog(4, n)
        break
"-----------------"
test()