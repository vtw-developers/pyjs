function test() {
    "--- test function ---";
    let param = [
        [88],
        [79],
        [7],
        [36],
        [23],
        [10],
        [27],
        [30],
        [71],
        [6]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    myexactlog(1, 0.0246 * (Math.pow(10, n) - 1 - (9 * n)));
    return 0.0246 * (Math.pow(10, n) - 1 - (9 * n));
}
"-----------------"

test()