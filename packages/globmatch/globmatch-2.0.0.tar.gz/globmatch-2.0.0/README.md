**[Installation](#installation)** |
**[Usage](#usage)** |
**[Testing](#testing)** |
**[License](#license)**

# [globmatch](https://github.com/vidartf/globmatch) - Matching paths against globs

[![codecov.io](https://codecov.io/github/vidartf/globmatch/coverage.svg?branch=master)](https://codecov.io/github/vidartf/globmatch?branch=master)

`globmatch` provides functions for matching a path against one ore more glob patterns in Python.
This differs from the `glob` module of the standard library, which matches a glob against the
file-tree on your system. `globmatch` does not interact with the filesystem at all, but relies on
generic matching. It also differs from the `fnmatch` module of the standard library in that it
accepts the double star (`**`) element, which matches zero or more directories. Additionally, the
star element (`*`) in `fnmatch` will also match across path separators. In `globmatch` the
star element matches zero or more characters of the current path element (directory/file name).


## Installation

Install globmatch with pip:

```bash
pip install globmatch
```

or for a development install:

```bash
pip install -e git+https://github.com/vidartf/globmatch#egg=globmatch
```

## Usage

```python
from globmatch import glob_match

# Some paths that match (returns True):
glob_match('.git/gitconfig/', ['.git'])
glob_match('foo/config', ['**/config'])
glob_match('foo/config/bar', ['**/config'])
glob_match('.git/gitconfig/', ['.git', '**/config'])
glob_match('foo/config/bar', ['.git', '**/config'])
glob_match('/.git/gitconfig/', ['**/.git'])

# Some paths that do not match (returns False):
glob_match('/.git/gitconfig/', ['.git'])   # Needs ** to match subdir of root dir
glob_match('foo/node_modules', ['node_modules'])   # Will not match subdir without preceding **

```



## Testing

Install the develop install with test requirements:

    pip install -e globmatch[test]

To run Python tests locally, enter on the command line: `pytest`

Install the [codecov browser extension](https://github.com/codecov/browser-extension#codecov-extension)
to view test coverage in the source browser on github.

## License

All code is licensed under the terms of the revised BSD license.

## Resources

- [Reporting Issues](https://github.com/vidartf/globmatch/issues)
