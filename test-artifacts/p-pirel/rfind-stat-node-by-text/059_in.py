def f_gold(a, b):
    if a == 0 or b == 0:
        myexactlog(1, 0)
        myexactlog(2, False)
        return False
    result = a * b
    myexactlog(3, result)
    if result >= 9223372036854775807 or result <= -9223372036854775808:
        myexactlog(4, 1)
        result = 0
        myexactlog(5, result)
    if a == (result // b):
        myexactlog(6, 2)
        print(result // b)
        myexactlog(7, False)
        return False
    else:
        pass