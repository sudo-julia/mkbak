# Functionality
`mkbak` makes backups of files in a given directory \[linux only]
Until recently (pre v0.5.0), `mkbak` was developed in my [`~/bin`](https://github.com/sudo-julia/bin) repo, so for old changes/commits, look there.


## Usage
1. Make the file executable:
  `chmod u+x "$path_to_mkbak"`
2. Invoke the program via the commandline
  `"$path_to_mkbak"`
  - Alternatively, you can use `python3 "$path_to_mkbak"` if you don't want to make the file executable
3. For options, run `mkbak --help`

## Requirements
  - [iterfzf](https://github.com/dahlia/iterfzf)
    - If you want the height option, use my [fork](https://github.com/sudo-julia/iterfzf)
  - Python3.6 or higher
  - A linux distribution to run the program on. I am considering developing a version for OSX and Windows as well.

## TODO
- [ ] Better "Usage" section
- [ ] Create `__main__.py`
- [ ] Write documentation
- [ ] Make tests
- [ ] Look into developing versions for BSD/OSX/Windows
- [ ] Github actions for linting

## Bugs
Open an issue or PR
