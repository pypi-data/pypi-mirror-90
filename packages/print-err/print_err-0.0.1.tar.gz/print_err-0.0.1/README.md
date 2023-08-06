# print_err

Command line utility and python library to print to standard error optionally exiting with a code.

# Install
```sh
pip install print_err
```

# Usage

As a python function
```python
from print_err import print_err
print_err("This messages goes to stderr")
print_err("This messages goes to stderr", exit_code=2)
```

As a command line utility
```sh
$ print_err "print to stderr and exit() with code 2" 2
```
