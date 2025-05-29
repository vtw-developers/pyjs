def test():
    f_gold()
"-----------------"
def f_gold():
    n = 0
    myexactlog(1, n)
    print(2, n)
    n = 1
    myexactlog(3, n)
    while n < 10:
        myexactlog(4, 0)
        n += 1
        myexactlog(5, n)
        break
"-----------------"
test()