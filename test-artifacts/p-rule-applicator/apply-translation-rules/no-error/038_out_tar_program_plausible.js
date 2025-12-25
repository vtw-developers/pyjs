function test() {
    "--- test function ---";
    let param = [
        [20],
        [6],
        [39],
        [80],
        [88],
        [7],
        [16],
        [27],
        [83],
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
    var res = 1;
    myexactlog(1, res);
    myexactlog(2, n % 2);
}
"-----------------"

test()