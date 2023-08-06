# DSKit

DSKit (Data Science Kit) is a Python package that provides tools for solving simple Data Science tasks.

# Installing

```bash
pip install dskit
```

# Tutorial

DSKit consists of two submodules:

* *dskit.frame* - contains a set of functions for *pandas.DataFrame* and *pandas.Series* manipulation.
* *dskit.tensor* - contains a set of functions for *numpy.ndarray* manipulation.

## *dskit.frame*

### *create_dummifier*

*create_dummifier* is less harmful alternative to *pd.get_dummies*. This function takes a *Dict[str, Tuple[object, ...]]* and returns *Callable[[pd.DataFrame], pd.DataFrame]*. Key of the dictionary is treated as a name of a column and value of the dictionary is treated as unique values of that column.
Each key and value of the dictionary are passed to *create_encoder* function. Bases on created encoders a new function is created which takes *pd.DataFrame* and returns *pd.DataFrame*. The returned function is a "dummify" function.

```python
frame = pd.DataFrame({"A": (1, 2, 2, 5, 5), "B": ("a", "a", "b", "c", "d")})
uniques: Dict[str, Tuple[object, ...]] = unique(frame)

dummify: Callable[[pd.DataFrame], pd.DataFrame] = create_dummifier(uniques)
print(dummify(frame))

#    A_1  A_2  A_5  B_a  B_b  B_c  B_d
# 0  1.0  0.0  0.0  1.0  0.0  0.0  0.0
# 1  0.0  1.0  0.0  1.0  0.0  0.0  0.0
# 2  0.0  1.0  0.0  0.0  1.0  0.0  0.0
# 3  0.0  0.0  1.0  0.0  0.0  1.0  0.0
# 4  0.0  0.0  1.0  0.0  0.0  0.0  1.0

other_frame = pd.DataFrame({"C": (True, True, False, True), "A": (1, 2, 3, 4)})
print(dummify(other_frame))

#    A_1  A_2  A_5      C
# 0  1.0  0.0  0.0   True
# 1  0.0  1.0  0.0   True
# 2  0.0  0.0  0.0  False
# 3  0.0  0.0  0.0   True

# notice, that columns are sorted alphabetically (C comes after A)
# you can pass sort_columns=False if you want to omit sorting
```

One of the reasons why *create_dummifier* is less harmful than *pd.get_dummies* is that it will not dummify new values. Thanks to that Machine Learning models will operate on data with the same number of dimensions regardless of new values presence in new portion of data.

```python
old_frame = pd.DataFrame({"B": ("a", "a", "b")})
new_frame = pd.DataFrame({"B": ("a", "b", "c")})

uniques: Dict[str, Tuple[object, ...]] = unique(old_frame)
dummify: Callable[[pd.DataFrame], pd.DataFrame] = create_dummifier(uniques)

print(dummify(new_frame))

#    B_a  B_b
# 0  1.0  0.0
# 1  0.0  1.0
# 2  0.0  0.0

print(pd.get_dummies(new_frame))

#    B_a  B_b  B_c
# 0    1    0    0
# 1    0    1    0
# 2    0    0    1
```

### *create_encoder*

*create_encoder* is a function used by *create_dummifier*. *create_encoder* takes a column name with a set of values and returns *Callable[[Tuple[object, ...]], pd.DataFrame]*. The returned function one-hot-encodes passed values. This function uses *sklearn.preprocessing.OneHotEncoder* under the hood.

```python
encoded: pd.DataFrame = create_encoder("A", (1, 2, 3))((1, 2, 3, 4, 5))
print(encoded)

#    A_1  A_2  A_3
# 0  1.0  0.0  0.0
# 1  0.0  1.0  0.0
# 2  0.0  0.0  1.0
# 3  0.0  0.0  0.0
# 4  0.0  0.0  0.0
```

### *unique*

*unique* is a function which takes *pd.DataFrame* and returns *Dict[str, Tuple[object, ...]]*. Key of the dictionary is a name of a column of the passed frame and value of the dictionary is unique values of that column.

```python
frame = pd.DataFrame({"A": (1, 2, 2, 5, 5), "B": ("a", "a", "b", "c", "d")})
uniques: Dict[str, Tuple[object, ...]] = unique(frame)

print(uniques)

# {'A': (1, 2, 5), 'B': ('a', 'b', 'c', 'd')}
```

## *dskit.tensor*

### *create_batches*

*create_batches* is a function which takes *Iterable[Tuple[np.ndarray, ...]]* with length of batches and returns an *Iterable[Tuple[np.ndarray, ...]]* of created batches.

```python
xs = np.arange(15).reshape(-1, 3)
ys = np.arange(10).reshape(-1, 2)

print(xs)

# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]

print(ys)

# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]
#  [8 9]]

for sub_xs, sub_ys in create_batches(zip(xs, ys), length=3):
  print(sub_xs)
  print(sub_ys)

  print()

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# [[0 1]
#  [2 3]
#  [4 5]]
#
# [[ 9 10 11]
#  [12 13 14]]
# [[6 7]
#  [8 9]]
```

### *cycle_tensor*

*cycle_tensor* is a "cycle" function used for tensors. This function takes a *np.ndarray* with *Tuple[int, ...]* and returns "cycled" *np.ndarray*.

```python
xs = np.arange(4).reshape(-1, 2)
print(xs)

# [[0 1]
#  [2 3]]

cycled_xs = cycle_tensor(xs, (3, 3))
print(cycled_xs)

# [[0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]]

zeros = cycle_tensor(0, (2, 2, 3))
print(zeros)

# [[[0 0 0]
#   [0 0 0]]
#
#  [[0 0 0]
#   [0 0 0]]]
```

### *expand_tail*

*expand_tail* is simply:

```python
def expand_tail(xs: Tuple[X, ...], length: int, filler: X) -> Tuple[X, ...]:
  count = max(length - len(xs), 0)

  fillers = repeat(filler)
  sliced_fillers = islice(fillers, count)

  expanded = chain(xs, sliced_fillers)
  return tuple(expanded)
```

Example of *expand_tail* usage:

```python
xs = expand_tail((1, 2), length=5, filler=3)
print(xs) # (1, 2, 3, 3, 3)
```

### *expand_tail_dimensions*

*expand_tail_dimensions* is simply:

```python
def expand_tail_dimensions(tensor: np.ndarray, length: int) -> np.ndarray:
  expanded_shape: Shape = expand_tail(tensor.shape, length, filler=1)
  return tensor.reshape(expanded_shape)
```

Example of *expand_tail_dimensions* usage:

```python
xs = np.arange(27).reshape(-1, 3, 3)
ys = expand_tail_dimensions(xs, 5)

print(ys.shape) # (3, 3, 3, 1, 1)
```

### *gridrange*

*gridrange* is a function similar to Python's *range* function. The difference between *gridrange* and *range* is that *gridrange* operates on *Tuple[int, ...]* instead of *int*.

```python
for x in gridrange((2, 3)):
  print(x)

# (0, 0)
# (0, 1)
# (0, 2)
# (1, 0)
# (1, 1)
# (1, 2)

for x in gridrange((1, 1), (3, 4)):
  print(x)

# (1, 1)
# (1, 2)
# (1, 3)
# (2, 1)
# (2, 2)
# (2, 3)

for x in gridrange((1, 1), (10, 20), (5, 5)):
  print(x)

# (1, 1)
# (1, 6)
# (1, 11)
# (1, 16)
# (6, 1)
# (6, 6)
# (6, 11)
# (6, 16)
```

### *iteraxis*

*iteraxis* is a function which takes *np.ndarray* and returns *Iterable[np.ndarray]* along passed axis. This function is similar to *np.apply_along_axis*. The difference between *iteraxis* and *np.apply_along_axis* is that *np.apply_along_axis* applies some function to arrays and *iteraxis* returns those arrays.

```python
xs = np.arange(27).reshape(-1, 3, 3)

for x in iteraxis(xs, axis=-1):
  print(x)

# [0 1 2]
# [3 4 5]
# [6 7 8]
# [ 9 10 11]
# [12 13 14]
# [15 16 17]
# [18 19 20]
# [21 22 23]
# [24 25 26]
```

### *move_tensor*

*move_tensor* is simply:

```python
def move_tensor(source: np.ndarray, destination: np.ndarray, coordinate: Optional[Coordinate] = None) -> np.ndarray:
  tensor = destination.copy()
  move_tensor_inplace(source, tensor, coordinate)

  return tensor
```
Example of *move_tensor* usage:

```python
xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

moved = move_tensor(xs, ys, coordinate=(1, 1))
print(moved)

# [[0 0 0]
#  [0 0 1]
#  [0 2 3]]
```

### *move_tensor_inplace*

*move_tensor_inplace* is a procedure which moves source *np.ndarray* to destination *np.ndarray* at coordinate *Tuple[int, ...]*. Only destination *np.ndarray* is modified. The coordinate is optional.

```python
xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

move_tensor_inplace(xs, ys)
print(ys)

# [[0 1 0]
#  [2 3 0]
#  [0 0 0]]
```

### *next_batch*

*next_batch* is a function used by *create_batches*. *next_batch* takes an *Iterable[Tuple[np.ndarray, ...]]* with length of batch and returns a next batch. The next batch might have smaller length than the passed one.

```python
xs = np.arange(15).reshape(-1, 3)
ys = np.arange(10).reshape(-1, 2)

print(xs)

# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]

print(ys)

# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]
#  [8 9]]

sub_xs, sub_ys = next_batch(zip(xs, ys), length=3)

print(sub_xs)
print(sub_ys)

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# [[0 1]
#  [2 3]
#  [4 5]]
```

### *slices*

*slices* is simply:

```python
RawSlice = Union[
  Tuple[Optional[int]],
  Tuple[Optional[int], Optional[int]],
  Tuple[Optional[int], Optional[int], Optional[int]]
]

def slices(xs: Iterable[RawSlice]) -> Tuple[slice, ...]:
  ys = starmap(slice, xs)
  return tuple(ys)
```

Example of *slices* usage:

```python
xs = np.arange(9).reshape(-1, 3)
ys = (1, None), (0, 1)

print(xs[slices(ys)])

# [[3]
#  [6]]
```
