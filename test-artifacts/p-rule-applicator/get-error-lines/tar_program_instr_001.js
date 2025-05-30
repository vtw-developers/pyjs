function test() {
    f_gold();
}
"-----------------"
function f_gold() {
    let n = 0;
    myexactlog(1, n);
    console.log(2, n);
    n = 1;
    myexactlog(3, n);
    while (n < 10) {
        myexactlog(4, 0);
        n += 'n';
        myexactlog(5, n);
        break;
    }
}
"-----------------"

test()