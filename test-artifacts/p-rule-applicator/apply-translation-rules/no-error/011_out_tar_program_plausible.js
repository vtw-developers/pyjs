function test() {
    "--- test function ---";
    let param = [
        [
            [5, 6, 8, 15, 42, 47, 49, 52, 53, 54, 55, 58, 58, 60, 60, 68, 70, 86, 94, 96, 97, 99], 18
        ],
        [
            [-87, 14, 24, 6, 58, 47, 45, 20, -37, -81, -8, -42, 83, -10, 17, -38], 14
        ],
        [
            [0, 0, 0, 0, 1, 1, 1, 1, 1], 4
        ],
        [
            [1, 16, 61, 64, 63, 69, 22, 93, 67, 76, 26, 16, 51, 86, 57, 29, 78, 92, 69, 47, 94, 62, 69, 76, 16, 90, 90, 48, 85, 39, 33, 94, 23, 10, 69, 34, 52, 95, 10, 19], 20
        ],
        [
            [-98, -96, -84, -76, -20], 2
        ],
        [
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1], 15
        ],
        [
            [7, 8, 10, 12, 21, 23, 24, 24, 26, 29, 34, 36, 36, 36, 37, 49, 55, 58, 62, 64, 68, 73, 74, 75, 81, 82, 87, 89, 90, 90, 93, 96, 96, 99, 99], 29
        ],
        [
            [-1, 5, -70, -83, 13, -38, -16, 12, -14, 41, 87, -81, 77, 0, 40, 89, 47, -24, -91, 99, -72, 28, -48], 13
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 24
        ],
        [
            [29, 37, 38, 83, 8], 2
        ]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        f_gold(...parameters_set);
        let result = parameters_set;
    }
}
"-----------------"
function f_gold(a, arr_size, ) {
    var lo = 0;
    myexactlog(1, lo);
    var hi = arr_size - 1;
    myexactlog(2, hi);
    var mid = 0;
    myexactlog(3, mid);
    while (mid <= hi) {
        myexactlog(4, 0);
        if (a[mid] === 0) {
            myexactlog(5, 0);
            [a[lo], a[mid]] = [a[mid], a[lo]];
            myexactlog(6, a);
            var lo = lo + 1;
            myexactlog(7, lo);
            var mid = mid + 1;
            myexactlog(8, mid);
        } else if (a[mid] === 1) {
            myexactlog(9, 0);
            var mid = mid + 1;
            myexactlog(10, mid);
        } else {
            myexactlog(11, 0);
            [a[mid], a[hi]] = [a[hi], a[mid]];
            myexactlog(12, a);
            var hi = hi - 1;
            myexactlog(13, hi);
        }
    }
}
"-----------------"

test()