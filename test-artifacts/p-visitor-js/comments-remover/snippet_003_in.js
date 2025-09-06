// comment
var lengthOfLongestSubstring = function(s) {  // comment
    const map = {};  // comment
    let offset = 0;  // comment
    return s.split('').reduce((max, value, i) => {  // comment
        offset = map[value] >= offset ? map[value] + 1 : offset;  // comment
        // comment
        // comment
        map[value] = i;  // comment
        return Math.max(max, i - offset + 1);  // comment
    }, 0);  // comment
};
// comment