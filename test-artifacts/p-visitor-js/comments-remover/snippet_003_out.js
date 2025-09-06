var lengthOfLongestSubstring = function(s) {
    const map = {};
    let offset = 0;
    return s.split('').reduce((max, value, i) => {
        offset = map[value] >= offset ? map[value] + 1 : offset;
        map[value] = i;
        return Math.max(max, i - offset + 1);
    }, 0);
};