function test() {
    "--- test function ---";
    let param = ["I love cinema.", "The vertex is S.", "I am single.", "My name is KG.", "I lovE cinema.", "GeeksQuiz. is a quiz site.", "I love Geeksquiz and Geeksforgeeks.", "  You are my friend.", "I love cinema", "Hello, world !", "Bond, James Bond.", "Trailing space ."];
    for (let i = 0; i < param.length; i++) {
        let parameters_set = param[i];
        let idx = i;
        let result = f_gold(parameters_set);
    }
}
"-----------------"
function f_gold(string_0, ) {
    var length = string_0.length;
    myexactlog(1, length);
    if (string_0[0] < "A" || string_0[0] > "Z") {
        myexactlog(2, 0);
        myexactlog(3, false);
        return false;
    }
    if (string_0[length - 1] !== ".") {
        myexactlog(4, 1);
        myexactlog(5, false);
        return false;
    }
    var prev_state = 0;
    myexactlog(6, prev_state);
    var curr_state = 0;
    myexactlog(7, curr_state);
    var index = 1;
    myexactlog(8, index);
    while (index < length) {
        myexactlog(9, 0);
        myexactlog(10, string_0[index]);
        break;
    }
}
"-----------------"

test()