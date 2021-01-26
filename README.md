# mkbak.py
`mkbak` makes backups of files in a given directory
Old changes can be found in my [`bin`](https://github.com/sudo-julia/bin) repo.


## Usage
1. Make the file executable:
  - `chmod u+x "$path_to_mkbak"`
  - Alternatively, you can use `'python3 "$path_to_mkbak"'` if you don't want to make the file executable
    - Optionally, set an alias for this to speed things up: `alias mkbak="python3 $path_to_mkbak"`
2. Add its containing folder to your \$PATH: `PATH="${path_to_mkbak}:${PATH}"`
3. Run the program with commandline options:
  - `mkbak -vi --path "$folder" -q 'pdf$'` will launch mkbak searching `$folder`, query files ending in 'pdf', ignore case distinctions in file names and print out any errors along with files successfully copied
4. For all options, run `mkbak --help`

## Requirements
  - [iterfzf](https://github.com/dahlia/iterfzf) for the fzf interface
    - If you want the height option, use my [fork](https://github.com/sudo-julia/iterfzf)
  - [rich](https://github.com/willmcgugan/rich) for formatting with `--verbose`
  - Python^3.7
  - Linux

## Bugs
Open an issue or PR

## Credits
Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
