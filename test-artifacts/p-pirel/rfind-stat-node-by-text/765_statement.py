while front != back:
    myexactlog(11, 0)
    front += 1
    myexactlog(12, front)
    if arr[front - 1] < arr[front]:
        myexactlog(13, 3)
        myexactlog(14, False)
        return False
    break