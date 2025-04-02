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
    console.log(JSON.stringify(helper, null, 2));
    for (let i = 0; i < nums.length; i++) {
        console.log(JSON.stringify('for #0', null, 2));
        let v = nums[i];
        console.log(JSON.stringify(v, null, 2));
        let num = target - v;
        console.log(JSON.stringify(num, null, 2));
        if (helper[num] !== undefined) {
            console.log(JSON.stringify('if #0', null, 2));
            return [helper[num], i];
        }
        helper[v] = i;
        console.log(JSON.stringify(helper, null, 2));
    }
}
"-----------------"
test()