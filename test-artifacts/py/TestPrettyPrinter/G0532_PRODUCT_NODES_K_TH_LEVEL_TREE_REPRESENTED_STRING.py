def f_gold(tree, k):
    level = -1
    product = 1
    n = len(tree)
    for i in range(0, n):
        if tree[i] == "(":
            level += 1
        elif tree[i] == ")":
            level -= 1
        else:
            if level == k:
                product *= int(tree[i]) - int("0")
    return product