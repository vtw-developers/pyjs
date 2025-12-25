function test() {
    "--- test function ---";
    let param = [
        [90],
        [95],
        [22],
        [29],
        [62],
        [40],
        [52],
        [21],
        [33],
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
    myexactlog(1, (n * n) + (n * n * n));
    return (n * n) + (n * n * n);
}
"-----------------"

test()