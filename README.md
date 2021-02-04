# mkbak.py

`mkbak` is a commandline utility to find files and create backups accordingly.  
It interfaces with `fzf` when finding the files, allowing you to interactively
select what to back up.

## Installation

### With Pip

- `pip install --user -U mkbak`

### Building from source

- `python3 setup.py sdist bdist_wheel`
- `pip install --user -U .`

## Usage

- Run `mkbak` to start recursively searching for files to backup
from your current directory
- For all options, run `mkbak --help`

Please note that the `--height` argument will be overridden if set to '100' and
the environment variable `$FZF_DEFAULT_OPTS` contains `--height` set to something
other than '100'

## Example

- `mkbak -vi --path "$folder" -q 'pdf$'`
will launch mkbak searching `$folder`
, query files ending in 'pdf', ignore case distinctions in file names and
print out any errors along with files successfully copied

## Requirements

- [mkbak-iterfzf](https://github.com/sudo-julia/mkbak-iterfzf)
for the fzf interface
- [rich](https://github.com/willmcgugan/rich) for formatting with `--verbose`
- Python^3.7
- Linux

## Changelog

See [CHANGELOG.md](https://github.com/sudo-julia/mkbak/blob/main/CHANGELOG.md)

## Bugs

Open an issue or PR

## ToDo

- [X] Package for pypi
- [X] Define entry point so the program can be run as `mkbak`
- [ ] Shell completions
- [ ] Add all options to README

## Credits

Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
