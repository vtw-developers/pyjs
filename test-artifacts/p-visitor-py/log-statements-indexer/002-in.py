def test():
    f_gold()
"-----------------"
def f_gold():
    myexactlog(3, 2, 1)
    print(4, 3, 2)
    myexactlog(a, b, c)
    print()
    myexactlog('a', 'b', 'c')
    print(4, 3, 2)
    myexactlog(a=1, b=2)
    print(4, 3, 2)
    myexactlog()
"-----------------"
test()