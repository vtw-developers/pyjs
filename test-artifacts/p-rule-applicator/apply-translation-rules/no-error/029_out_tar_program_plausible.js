function test() {
    "--- test function ---";
    let param = [
        [94],
        [94],
        [79],
        [39],
        [16],
        [90],
        [64],
        [76],
        [83],
        [47],
        [-1]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    var odd_count = 0;
    myexactlog(1, odd_count);
    var even_count = 0;
    myexactlog(2, even_count);
    if (n < 0) {
        myexactlog(3, 0);
        var n = -n;
        myexactlog(4, n);
    }
    if (n === 0) {
        myexactlog(5, 1);
        myexactlog(6, 1);
        return 1;
    }
    if (n === 1) {
        myexactlog(7, 2);
        myexactlog(8, 0);
        return 0;
    }
    while (n) {
        myexactlog(9, 0);
        if (n & 1) {
            myexactlog(10, 3);
            var odd_count = odd_count + 1;
            myexactlog(11, odd_count);
        }
        if (n & 2) {
            myexactlog(12, 4);
            var even_count = even_count + 1;
            myexactlog(13, even_count);
        }
        var n = n >> 2;
        myexactlog(14, n);
    }
    myexactlog(15, f_gold(Math.abs(odd_count - even_count)));
    return f_gold(Math.abs(odd_count - even_count));
}
"-----------------"

test()