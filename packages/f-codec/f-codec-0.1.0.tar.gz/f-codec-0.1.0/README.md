# Python `f` Codec

Wrap lonesome f-strings in `print()`.

## How to install

```sh
> python3 -m pip install f-codec
```

## Why?

```python
# -*- coding: f -*-

def dictionary(inst, depth=0):
    ಠ_ಠ = '    ' * depth

    f''' {{
'''

    for name, val in inst.items():
        if isinstance(val, dict):
            f'''
    {name} =
''' > ಠ_ಠ
            dictionary(val, depth + 1)
        else:
            f'''
    {name} = {val},
''' > ಠ_ಠ

    f'''
}}
''' > ಠ_ಠ

decl = {
    'a': 1,
    'b': 2,
    'c': { 'a': 3, 'b': 4 },
    'd': { 'a': 5, 'b': { 'a': 6, 'b': 7 }, 'c': 8 },
    'e': 9
}

f'''
decl =
'''
dictionary(decl)
```

```sh
> python3 test.py

decl = {
    a = 1,
    b = 2,
    c = {
        a = 3,
        b = 4,
    }
    d = {
        a = 5,
        b = {
            a = 6,
            b = 7,
        }
        c = 8,
    }
    e = 9,
}
```
