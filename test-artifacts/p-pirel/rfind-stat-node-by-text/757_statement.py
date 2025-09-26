for i in range(1, n):
    myexactlog(8, 1)
    if price[i] < min_price:
        myexactlog(9, 1)
        min_price = price[i]
        myexactlog(10, min_price)
    profit[i] = max(profit[i - 1], profit[i] + (price[i] - min_price))
    myexactlog(11, profit)
    break