function test() {
    "--- test function ---";
    let param = [
        [18, 94],
        [23, 36],
        [24, 22],
        [75, 92],
        [25, 43],
        [57, 32],
        [31, 57],
        [8, 17],
        [12, 76],
        [74, 70],
        [4, -1]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(x, y, ) {
    if (y === 0) {
        myexactlog(1, 0);
        myexactlog(2, 0);
        return 0;
    }
    if (y > 0) {
        myexactlog(3, 1);
        var retval_1 = x + f_gold(x, y - 1);
        myexactlog(4, retval_1);
        myexactlog(5, retval_1);
        return retval_1;
    } else {
        myexactlog(6, 0);
        var retval_2 = -f_gold(x, -y);
        myexactlog(7, retval_2);
        myexactlog(8, retval_2);
        return retval_2;
    }
}
"-----------------"

test()