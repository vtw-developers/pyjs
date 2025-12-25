function test() {
    "--- test function ---";
    let param = [
        [4, 43, 24],
        [60, 48, 98],
        [92, 21, 69],
        [73, 79, 38],
        [58, 38, 30],
        [82, 26, 12],
        [53, 10, 17],
        [57, 37, 26],
        [47, 91, 99],
        [83, 3, 64],
        [0]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, a = 0, b = 1, ) {
    if (n === 0) {
        myexactlog(1, 0);
        myexactlog(2, a);
        return a;
    }
    if (n === 1) {
        myexactlog(3, 1);
        myexactlog(4, b);
        return b;
    }
    var retval_1 = f_gold(n - 1, b, a + b);
    myexactlog(5, retval_1);
    myexactlog(6, retval_1);
    return retval_1;
}
"-----------------"

test()