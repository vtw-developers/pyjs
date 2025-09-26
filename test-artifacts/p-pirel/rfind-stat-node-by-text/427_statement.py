for n in range(7, N + 1):
    screen[n - 1] = max(2 * screen[n - 4], max(3 * screen[n - 5], 4 * screen[n - 6]))