function test() {
    "--- test function ---";
    let param = [
        ["t a"],
        ["77 78 2 600 7"],
        ["011 10 10"],
        ["kV Co O iR"],
        ["2"],
        ["0 11"],
        ["Y sT wgheC"],
        ["58 824 6"],
        ["00 100 001 0111"],
        ["Q"]
    ];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(...parameters_set);
    }
}
"-----------------"
function f_gold(str_0, ) {
    var result = "";
    myexactlog(1, result);
    myexactlog(2, true);
}
"-----------------"

test()