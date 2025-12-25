function test() {
    "--- test function ---";
    let param = [
        [72],
        [90],
        [61],
        [28],
        [70],
        [13],
        [7],
        [98],
        [99],
        [67]
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
    for (let i = 0; i < n; i++) {
        myexactlog(2, 0);
        var res = res * (2 * n - i);
        myexactlog(3, res);
        res /= i + 1;
        myexactlog(4, res);
    }
    myexactlog(5, res / (n + 1));
    return res / (n + 1);
}
"-----------------"

test()