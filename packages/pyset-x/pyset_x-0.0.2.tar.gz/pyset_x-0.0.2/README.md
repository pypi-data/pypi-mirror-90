# pyset_x

This is `set -x` in Bash, but for Python. Before a line of code is executed, it will be printed. The idea is for quick debugging of actual code flow, instead of having to put `print` calls in all your `if/elif/else` blocks etc.

## Example
```python
from pyset_x import annotate_function
@annotate_function
def func():
    a = 1 + 1
    return a
func()
```

Will print

```
a = 1 + 1                                                                                                              
return a 
```

