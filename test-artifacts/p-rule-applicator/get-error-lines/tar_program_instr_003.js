function test() {
    "--- test function ---";
    let param = [
        [95],
        [48],
        [3],
        [10],
        [82],
        [1],
        [77],
        [99],
        [23],
        [61]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(n, ) {
    var count = 0;
    myexactlog(1, count);
    var ans = 1;
    myexactlog(2, ans);
    while (n % 2 === 0) {
        myexactlog(3, 0);
        var count = count + 1;
        myexactlog(4, count);
        var n = Math.floor(n / 2);
        myexactlog(5, n);
    }
    if (count % 2 !== 0) {
        myexactlog(6, 0);
        var ans = ans * 2;
        myexactlog(7, ans);
    }
    for (var i = 3; i <= Math.floor(Math.sqrt(n)); i += 2) {
        myexactlog(8, 0);
        var count = 0;
        myexactlog(9, count);
        while (n % i === 0) {
            myexactlog(10, 1);
            var count = count + 1;
            myexactlog(11, count);
            var n = Math.floor(n / i);
            myexactlog(12, n);
        }
        if (count % 2 !== 0) {
            myexactlog(13, 1);
            var ans = ans * i;
            myexactlog(14, ans);
        }
    }
    if (n > 2) {
        myexactlog(15, 2);
        var ans = ans * n;
        myexactlog(16, ans);
    }
    myexactlog(17, ans);
    return ans;
}
"-----------------"

test()