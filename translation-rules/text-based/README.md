# About
Contains configurations for text-based transformation.

# Contents
## rec_call_replacements.json
```py
def f_gold(n):
  return f_gold(n - 1)
```
```json
{
  "G0011": {
    "f_gold": {
      "f_gold": {
        "py": 1,
        "js": 1
      }
    }
  }
}
```
Inside function definition of `f_gold`, replace invocations to `f_gold` with `1`.

## iter_collection.json
```py
for x in frequency:
  pass
for x in sorted(frequency.keys()):
  pass
```
```json
{
  "G0010": {
    "type": "for_key_in_dict",
    "key_var": "x",
    "dict_var": "frequency"
  }
}
```
Replace all occurences of loops like `for <key_var> in <dict_var>` to
`for <key_var> in sorted(<dict_var>.keys())`.
