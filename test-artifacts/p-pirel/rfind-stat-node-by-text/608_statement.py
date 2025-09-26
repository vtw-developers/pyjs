for j in range(i - 1, -2, -1):
    result[j + 1] = int("0" + str(count))
    count += 1
    if j >= 0 and seq[j] == "I":
        break