def test():
    args_sets = [[[2, 7, 11, 15], 9], [[3, 2, 4], 6], [[3, 3], 6]]
    for idx, args_set in enumerate(args_sets):
        f_gold(*args_set)
"-----------------"
### twoSum
from typing import *
def f_gold(nums: List[int], target: int) -> List[int]:
    helper = {}
    myexactlog(helper)
    for i, v in enumerate(nums):
        myexactlog(0)
        num = target - v
        myexactlog(num)
        if num in helper:
            myexactlog(0)
            myexactlog([helper[num], i])
            return [helper[num], i]
        helper[v] = i
        myexactlog(helper)
"-----------------"
test()