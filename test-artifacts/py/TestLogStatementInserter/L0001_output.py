def test():
    args_sets = [[[2, 7, 11, 15], 9], [[3, 2, 4], 6], [[3, 3], 6]]
    for idx, args_set in enumerate(args_sets):
        f_gold(*args_set)
"-----------------"
### twoSum
from typing import *
def f_gold(nums: List[int], target: int) -> List[int]:
    helper = {}
    pirel_log_obj(helper)
    for i, v in enumerate(nums):
        pirel_log_obj('for #0')
        num = target - v
        pirel_log_obj(num)
        if num in helper:
            pirel_log_obj('if #0')
            pirel_log_obj([helper[num], i])
            return [helper[num], i]
        helper[v] = i
        pirel_log_obj(helper)
"-----------------"
test()