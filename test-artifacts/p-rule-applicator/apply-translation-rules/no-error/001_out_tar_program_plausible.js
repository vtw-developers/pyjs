function test() {
    "--- test function ---";
    let param = [
        [0],
        [-21],
        [7],
        [63],
        [84],
        [73],
        [81],
        [-10],
        [47],
        [23]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(num, ) {
    if (num < 0) {
        myexactlog(1, 0);
        myexactlog(2, f_gold(-num));
        return f_gold(-num);
    }
    if (num === 0 || num === 7) {
        myexactlog(3, 1);
        myexactlog(4, true);
        return true;
    }
    if (num < 10) {
        myexactlog(5, 2);
    }
}
"-----------------"

test()