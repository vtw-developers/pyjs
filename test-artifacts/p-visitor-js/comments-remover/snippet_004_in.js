var threeSum = function(nums) {  // comment
    /*
    multiline comment
    */
    const result = [];  // comment
    nums.sort((a, b) => a - /*comment*/ b);
    for (let i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        let j = i + 1;  /*comment*/
        let k = nums.length - 1;
/*comment*/
        while (j < k) {
            const sum = nums[i] + nums[j] + nums[k];
            if (!sum) {
                result.push([nums[i], nums[j], nums[k]]);
                j++;
                k--;
                while (j < k && nums[j] === nums[j - 1]) {
                    j++;
                }/*comment*/
                while (j < k && nums[k] === nums[k + 1]) {
                    k--;/*comment*/
                }
            } else {
                /*comment*/sum < 0 ? j++ : k--;
            }/*comment*/
        }/*comment*/
    }
    return result;
};/*comment*//*comment*//*comment*//*comment*//*comment*/