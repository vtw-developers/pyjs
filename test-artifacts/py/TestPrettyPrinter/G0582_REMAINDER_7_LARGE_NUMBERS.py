def f_gold(num):
    series = [1, 3, 2, -1, -3, -2]
    series_index = 0
    result = 0
    for i in range((len(num) - 1), -1, -1):
        digit = ord(num[i]) - 48
        result += digit * series[series_index]
        series_index = (series_index + 1) % 6
        result %= 7
    if result < 0:
        result = (result + 7) % 7
    return result