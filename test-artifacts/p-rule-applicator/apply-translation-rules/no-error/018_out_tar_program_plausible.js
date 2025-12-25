function test() {
    "--- test function ---";
    let param = [
        [85],
        [86],
        [3],
        [35],
        [59],
        [38],
        [33],
        [15],
        [75],
        [74]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    if (n < 3) {
        myexactlog(1, 0);
        myexactlog(2, n);
        return n;
    } else if (n >= 3 && n < 10) {
        myexactlog(3, 0);
        myexactlog(4, n - 1);
        return n - 1;
    }
    var po = 1;
    myexactlog(5, po);
    while (Math.floor(n / po) > 9) {
        myexactlog(6, 0);
        var po = po * 10;
        myexactlog(7, po);
    }
    var msd = Math.floor(n / po);
    myexactlog(8, msd);
    if (msd !== 3) {
        myexactlog(9, 1);
        myexactlog(10, f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po));
        return f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po);
    } else {
        myexactlog(11, 0);
        myexactlog(12, f_gold(msd * po - 1));
        return f_gold(msd * po - 1);
    }
}
"-----------------"

test()