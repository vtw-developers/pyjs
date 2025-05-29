def test():
    f_gold()
"-----------------"
def f_gold():
    n = 0
    myexactlog(n)
    print(n)
    n = 1
    myexactlog(n)
    while n < 10:
        myexactlog(0)
        n += 1
        myexactlog(n)
        break
"-----------------"
test()