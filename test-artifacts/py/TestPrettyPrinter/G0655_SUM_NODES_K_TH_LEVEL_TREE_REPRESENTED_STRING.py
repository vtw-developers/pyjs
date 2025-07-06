def f_gold(tree, k):
    level = -1
    sum = 0
    n = len(tree)
    for i in range(n):
        if tree[i] == "(":
            level += 1
        elif tree[i] == ")":
            level -= 1
        else:
            if level == k:
                sum += ord(tree[i]) - ord("0")
    return sum