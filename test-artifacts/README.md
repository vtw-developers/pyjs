# About
Stores files that are used in unit tests.

# Contents

## TestPrettyPrinter
- Test inputs used for testing `PrettyPrinter` class.
- Copied from `benchmarks/leetcode/pysep` directory.
- The programs are slightly modified to conform to the pretty printing rules of `PrettyPrinter` class:
  - Spaces are inserted around `**` operator
  - Some comments are removed
  - Removed space characters around colons is slice node.
  - Reformatted `List[tuple]`, `dict`
  - Reformatted condition in `if_statement`
  - Put parentheses around `generator_expression`
  - etc.
  
  To see the exact changes, run `diff` command.
