function test() {
    "--- test function ---";
    let param = [
        ["", 0, -1],
        ["x", 0, 0],
        ["1101010101111110", 0, 15]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(str_0, l, h, ) {}
"-----------------"

test()