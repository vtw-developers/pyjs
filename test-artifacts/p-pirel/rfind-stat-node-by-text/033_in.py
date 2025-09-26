def f_gold(price, n):
    profit = [0] * n
    myexactlog(1, profit)
    max_price = price[n - 1]
    myexactlog(2, max_price)
    for i in range(n - 2, 0, -1):
        myexactlog(3, 0)
        if price[i] > max_price:
            myexactlog(4, 0)
            max_price = price[i]
            myexactlog(5, max_price)
        profit[i] = max(profit[i + 1], max_price - price[i])
        myexactlog(6, profit)
        break
    min_price = price[0]