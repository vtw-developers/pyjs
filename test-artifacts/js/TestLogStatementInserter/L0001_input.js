function test() {
    let args_sets = [
        [
            [2, 7, 11, 15], 9
        ],
        [
            [3, 2, 4], 6
        ],
        [
            [3, 3], 6
        ]
    ];
    for (let idx = 0; idx < args_sets.length; idx++) {
        let args_set = args_sets[idx];
        f_gold(...args_set);
    }
}
"-----------------"

function f_gold(nums, target) {
let helper = {};
for (let i = 0; i < nums.length; i++) {
    let v = nums[i];
    let num = target - v;
    if (helper[num] !== undefined) {
        return [helper[num], i];
    }
    helper[v] = i;
}
}
"-----------------"
test()