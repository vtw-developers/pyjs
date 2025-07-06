def f_gold(s):
    length = int(s / 3)
    s -= length
    breadth = s / 2
    height = s - breadth
    return int(length * breadth * height)