'\n    :type target: int\n    :type position: List[int]\n    :type speed: List[int]\n    :rtype: int\n    '
car = [(pos, spe) for pos, spe in zip(position, speed)]
car.sort(reverse=True)
time = [(target - pos) / spe for pos, spe in car]
ls = []
for i in time:
    if not ls:
        ls.append(i)
    elif i > ls[-1]:
        ls.append(i)
return len(ls)