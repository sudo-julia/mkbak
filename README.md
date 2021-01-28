# mkbak.py

`mkbak` makes backups of files in a given directory  
old changes can be found in my [`bin`](https://github.com/sudo-julia/bin) repo.

## Installation

`pip install --user mkbak`

## Usage

- Run the program with commandline options:
  - `python3 -m mkbak -vi --path "$folder" -q 'pdf$'`
will launch mkbak searching `$folder`
, query files ending in 'pdf', ignore case distinctions in file names and
print out any errors along with files successfully copied
- For all options, run `mkbak --help`

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

## Credits

Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
