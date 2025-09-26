def f_gold(num):
    num = list(num)
    n = len(num)
    rightMin = [0] * n
    right = 0
    rightMin[n - 1] = -1
    right = n - 1
    for i in range(n - 2, 0, -1):
        if num[i] > num[right]:
            rightMin[i] = right
        else:
            rightMin[i] = -1
            right = i
    small = -1
    for i in range(1, n):
        if num[i] != "0":
            if small == -1:
                if num[i] < num[0]:
                    small = i
            elif num[i] < num[small]:
                small = i