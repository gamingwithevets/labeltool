A module for loading label files. Currently, it only supports loading labels from a file-like object.  
(command-line interface coming soon)

## Syntax
Label files use the syntax created by [user202729](https://github.com/user202729):
```
01234		function_label
f_02345		function_label
.l_002		.local_label
d_45678		data_label
data_label.1		bit_data_label
# comment
```

Note that there should not be any duplicate labels in the provided labels file. If there are, the first label found will be used.

## Label format
### Function and local labels
```
addr: {name, is_func}
```
If `is_func` is `False`, there will be 2 extra items.
```
addr: {name, False, parent_addr, bcond_jmp_list}
```
### Data labels
```
addr: name
```
### Bit data labels
```
bit_string: name
```

## Functions
### `load_label(f, start)`
Loads labels from a file-like object.

Arguments:
- `f`: A file-like object to load label data from. Should be in text read mode.
- `start`: The starting address.

Returns: 3 dictionaries for function + local labels, data labels and bit data labels respectively.
