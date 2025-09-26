for i in range(n):
    print(i + 1, "         ", processSize[i], end="     ")
    if allocation[i] != -1:
        print(allocation[i] + 1)
    else:
        print("Not Allocated")