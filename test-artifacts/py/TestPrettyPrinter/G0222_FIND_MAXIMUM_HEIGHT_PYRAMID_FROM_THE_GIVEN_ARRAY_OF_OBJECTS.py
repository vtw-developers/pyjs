def f_gold(boxes, n):
    boxes.sort()
    ans = 1
    prev_width = boxes[0]
    prev_count = 1
    curr_count = 0
    curr_width = 0
    for i in range(1, n):
        curr_width += boxes[i]
        curr_count += 1
        if curr_width > prev_width and curr_count > prev_count:
            prev_width = curr_width
            prev_count = curr_count
            curr_count = 0
            curr_width = 0
            ans += 1
    return ans