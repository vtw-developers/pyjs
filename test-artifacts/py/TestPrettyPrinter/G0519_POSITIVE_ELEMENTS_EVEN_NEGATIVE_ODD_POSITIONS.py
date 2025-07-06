def f_gold(a, size):
    positive = 0
    negative = 1
    while True:
        while positive < size and a[positive] >= 0:
            positive = positive + 2
        while negative < size and a[negative] <= 0:
            negative = negative + 2
        if positive < size and negative < size:
            temp = a[positive]
            a[positive] = a[negative]
            a[negative] = temp
        else:
            break