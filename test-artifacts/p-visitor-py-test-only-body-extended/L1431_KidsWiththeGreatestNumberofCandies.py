mx = max(candies)
return [candy + extraCandies >= mx for candy in candies]