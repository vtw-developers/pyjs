function test() {
    "--- test function ---";
    let param = [
        [39],
        [79],
        [7],
        [76],
        [48],
        [18],
        [58],
        [17],
        [36],
        [5]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    if (n === 0 || n === 1) {
        myexactlog(1, 0);
    }
}
"-----------------"

test()