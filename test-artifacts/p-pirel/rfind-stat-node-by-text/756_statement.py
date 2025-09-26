if sum1 >= sum2 and sum1 >= sum3:
    sum1 -= stack1[top1]
    top1 = top1 + 1
elif sum2 >= sum3 and sum2 >= sum3:
    sum2 -= stack2[top2]
    top2 = top2 + 1
else:
    sum3 -= stack3[top3]
    top3 = top3 + 1