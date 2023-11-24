A module for loading label files. Currently, it only supports loading labels from a file-like object.  
(command-line interface coming soon)

## Syntax
Label files use the syntax created by [user202729](https://github.com/user202729):
```
01234		function_label
f_02345		function_label
.l_002		.local_label
d_45678		data_label		# comment
# comment
```

Note that there should not be any duplicate labels in the provided labels file. If there are, the first label found will be used.

## Functions
### `load_label(f)`
Loads labels from a file-like object.

Arguments:
- `f`: A file-like object to load label data from. Should be in text read mode.

Returns: 2 dictionaries for function + local labels and data labels respectively.
