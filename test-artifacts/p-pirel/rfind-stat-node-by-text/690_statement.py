for i in range(1, n):
    if num[i] != "0":
        if small == -1:
            if num[i] < num[0]:
                small = i
        elif num[i] < num[small]:
            small = i