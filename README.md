# mkbak.py

`mkbak` is a commandline utility to find files and create backups accordingly.  
It interfaces with `fzf` when finding the files, allowing you to interactively
select what to back up.

## Installation

`pip install --user -U mkbak`

## Usage

- Run `python3 -m mkbak` to start recursively searching for files to backup
from your current directory
  - You can alias this to make the process quicker: `alias mkbak='python3 -m mkbak'`
- For all options, run `mkbak --help`

### Example

- `python3 -m mkbak -vi --path "$folder" -q 'pdf$'`
will launch mkbak searching `$folder`
, query files ending in 'pdf', ignore case distinctions in file names and
print out any errors along with files successfully copied

## Requirements

- [mkbak-iterfzf](https://github.com/sudo-julia/mkbak-iterfzf)
for the fzf interface
- [rich](https://github.com/willmcgugan/rich) for formatting with `--verbose`
- Python^3.7
- Linux

## Bugs

Open an issue or PR

## ToDo

- [X] Package for pypi
- [ ] Rewrite README in .rst for rendering on PyPi
- [ ] Add all options to README
- [ ] Define entry point so the program can be run as `mkbak`

## Credits

Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
