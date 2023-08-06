![test](https://github.com/davips/lange/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/lange/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/lange)

# lange
Lazy lists (i.e. Haskell-like ranges) for Python.

### Features
 * Stable floating-point range generation, e.g.: `0.8 - 0.6 == 0.2` up to 28 digits (customizable).
 * Infinite `[1 2 ...]` or bounded.
 * O(1) access/evaluation `lst[3443]`


### Examples

**Arithmetic Progression** <details>
<p>

```python3

# "Forbidden" syntax.
import lange
print(-[0.6, 0.8, ..., 2])
# [0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0]
```

```python3

# Conservative syntax.
from lange_ import a_
print(a_[0.6, 0.8, ..., 2])
# [0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0]
```

```python3

pr = a_[0.6, 0.8, ...]
print(pr[:5])
# [0.6 0.8 1.0 1.2 1.4]
```


</p>
</details>

**Geometric Progression** <details>
<p>

```python3

# "Forbidden" syntax.
import lange
print(~[0.4, 0.8, ..., 2])
# [0.4 0.8 1.6]
```

```python3

# Conservative syntax.
from lange_ import g_
print(g_[0.4, 0.8, ..., 2])
# [0.4 0.8 1.6]
```

```python3

pr = g_[0.4, 0.8, ...]
print(pr[:5])
# [0.4 0.8 1.6 3.2 6.4]
```


</p>
</details>
