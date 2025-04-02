def test():
    args_sets = [[[2, 7, 11, 15], 9], [[3, 2, 4], 6], [[3, 3], 6]]
    for idx, args_set in enumerate(args_sets):
        f_gold(*args_set)
"-----------------"
### twoSum
from typing import *
def f_gold(nums: List[int], target: int) -> List[int]:
    import json
    helper = {}
    print(json.dumps(helper, sort_keys=True, indent=2))
    for i, v in enumerate(nums):
        print(json.dumps('for #0', sort_keys=True, indent=2))
        num = target - v
        print(json.dumps(num, sort_keys=True, indent=2))
        if num in helper:
            print(json.dumps('if #0', sort_keys=True, indent=2))
            return [helper[num], i]
        helper[v] = i
        print(json.dumps(helper, sort_keys=True, indent=2))
"-----------------"
test()