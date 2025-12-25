function test() {
    "--- test function ---";
    let param = [
        ["amazon", "azonam"],
        ["onamaz", "amazon"],
        ["amazon", "azoman"],
        ["ab", "ab"],
        ["737009", "239119"],
        ["000110", "01111"],
        ["l", "YVo hqvnGxow"],
        ["4420318628", "52856"],
        ["11011111000000", "10"],
        [" pvFHANc", "xBIDFbiGb"]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(str1, str2, ) {
    myexactlog(1, str2.length);
}
"-----------------"

test()