def f_gold(input_0, unlock_code):
    rotation = 0
    myexactlog(1, rotation)
    while input_0 > 0 or unlock_code > 0:
        myexactlog(2, 0)
        input_digit = input_0 % 10
        myexactlog(3, input_digit)
        code_digit = unlock_code % 10
        myexactlog(4, code_digit)
        rotation += min(abs(input_digit - code_digit), 10 - abs(input_digit - code_digit))
        myexactlog(5, rotation)
        input_0 = int(input_0 / 10)