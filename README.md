# mkbak.py

[![PyPI version](https://badge.fury.io/py/mkbak.svg)](https://badge.fury.io/py/mkbak)

`mkbak` is a commandline utility to painlessly create file backups.  
It interfaces with `fzf` as a menu for file selection, allowing you to
interactively choose which files to back up.

## Installation

### With Pip

- `pip install --user -U mkbak`

### Building from source

- Download the repository:
  - `git clone https://github.com/sudo-julia/mkbak`
- Enter the repo
  - `cd mkbak`
- Build the package
  - `python3 setup.py sdist bdist_wheel`
- Install from the local build
  - `pip install --user -U .`

## Usage

- Run `mkbak [options]` to start searching for files to backup
from your current directory

### Arguments

- `-h|--help` display all options
- `--version`             print version information
- `-d, --delete`          iterate through '.bak' files to delete
  - please note that this search can take a while, as it's only returning
'.bak' files
- `-q [QUERY], --query [QUERY]` start the finder with the given query
- `-a, --all`             show hidden and 'dot' files
- `-e, --exact`           exact matching
- `--height [HEIGHT]`       display fzf window with the given height
  - Please note that the `--height` argument will be overridden if set to '100' and
the environment variable `$FZF_DEFAULT_OPTS` contains `--height` set to something
other than '100'
- `-i, --ignore_case`     ignore case distinction
- `--no_mouse`            disable mouse interaction
- `--no_recursion`        run mkbak without recursing through subdirectories
- `-p [PATH], --path [PATH]`  directory to iterate through (default '.')
- `--preview [PREVIEW]`     starts external process with current line as arg
- `--print_query`         print query as the first line
- `--prompt [PROMPT]`       input prompt (default: '> ')
- `-v, --verbose`         explain what is being done

### Example

- `mkbak -vi --path "$folder" -q 'pdf$'`
will launch mkbak searching `$folder`,
query files ending in 'pdf', ignore case distinctions in file names and
print out any errors along with files successfully copied

## Requirements

- [mkbak-iterfzf](https://github.com/sudo-julia/mkbak-iterfzf)
for the fzf interface
- [rich](https://github.com/willmcgugan/rich) for text formatting
- Python^3.7
- Linux

## Changelog

See [CHANGELOG.md](https://github.com/sudo-julia/mkbak/blob/main/CHANGELOG.md)

## Bugs

Open an issue or PR

## ToDo

- [X] Package for pypi
- [X] Define entry point so the program can be run as `mkbak`
- [X] Add all options to README
- [ ] Shell completions

## Credits

Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
