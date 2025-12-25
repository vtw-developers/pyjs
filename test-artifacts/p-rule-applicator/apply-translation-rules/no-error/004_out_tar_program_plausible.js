function test() {
    "--- test function ---";
    let param = [
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
        [11]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    var retval_1 = (n == 1 || n == 0) ? 1 : n * f_gold(n - 1);
    myexactlog(1, retval_1);
}
"-----------------"

test()