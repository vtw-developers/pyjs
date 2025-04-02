expected = sorted(heights)
return sum((a != b for a, b in zip(heights, expected)))