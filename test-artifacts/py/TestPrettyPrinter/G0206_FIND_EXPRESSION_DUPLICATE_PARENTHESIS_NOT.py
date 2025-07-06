def f_gold(string):
    Stack = []
    for ch in string:
        if ch == ")":
            top = Stack.pop()
            elementsInside = 0
            while top != "(":
                elementsInside += 1
                top = Stack.pop()
            if elementsInside < 1:
                return True
        else:
            Stack.append(ch)
    return False