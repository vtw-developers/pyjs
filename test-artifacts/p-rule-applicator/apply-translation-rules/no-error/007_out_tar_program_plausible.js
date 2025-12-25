function test() {
    "--- test function ---";
    let param = [
        [
            [], 0
        ],
        [
            [1, 0], 2
        ],
        [
            [1, 0, 1, 0], 4
        ]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(arr, n, ) {
    var hash_map = {};
    myexactlog(1, hash_map);
    var curr_sum = 0;
    myexactlog(2, curr_sum);
    var max_len = 0;
    myexactlog(3, max_len);
    var ending_index = -1;
    myexactlog(4, ending_index);
    for (var i = 0; i < n; i++) {
        myexactlog(5, 0);
        if (arr[i] === 0) {
            myexactlog(6, 0);
            arr[i] = -1;
            myexactlog(7, arr);
        } else {
            myexactlog(8, 0);
            var __tmp = (arr[i] = 1);
            myexactlog(9, arr);
        }
    }
    for (var i = 0; i < n; i++) {
        myexactlog(10, 1);
        var curr_sum = curr_sum + arr[i];
        myexactlog(11, curr_sum);
        if (curr_sum === 0) {
            myexactlog(12, 1);
            var max_len = i + 1;
            myexactlog(13, max_len);
            var ending_index = i;
            myexactlog(14, ending_index);
        }
        if (Object.prototype.hasOwnProperty.call(hash_map, curr_sum)) {
            myexactlog(15, 2);
            myexactlog(16, hash_map[curr_sum]);
        } else {
            myexactlog(17, 1);
        }
        break;
    }
}
"-----------------"

test()