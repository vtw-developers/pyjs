function test() {
    "--- test function ---";
    let param = [
        ["()"],
        ["))(("],
        ["())"],
        ["(()"],
        ["(()()())"],
        ["))())(()(())"],
        ["))(())(("],
        ["49"],
        ["00001111"],
        ["KDahByG "],
        [""]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(s, ) {
    myexactlog(1, s.length);
}
"-----------------"

test()