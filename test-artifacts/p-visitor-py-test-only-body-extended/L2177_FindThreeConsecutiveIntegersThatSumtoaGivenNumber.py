a, b = divmod(num, 3)
return [] if b else [a - 1, a, a + 1]