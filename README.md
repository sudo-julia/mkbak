# mkbak.py

![PyPI](https://img.shields.io/pypi/v/mkbak?color=informational&style=flat)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkbak)
![PyPI - License](https://img.shields.io/pypi/l/mkbak)
![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/g/sudo-julia/mkbak/main?style=flat)
![PyPI - Format](https://img.shields.io/pypi/format/mkbak?color=informational)
![GitHub last commit](https://img.shields.io/github/last-commit/sudo-julia/mkbak)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/sudo-julia/mkbak)

`mkbak` is a commandline utility to painlessly create file backups.  
It interfaces with `fzf` as a menu for file selection, allowing you to
quickly select files.

## Installation

### With Pip

- `pip install --user -U mkbak`

### With Poetry

- Download the repository:
  - `git clone https://github.com/sudo-julia/mkbak`
- Enter the repo
  - `cd mkbak`
- Install dependencies:
  - `poetry install`
- Run mkbak:
  - `poetry run mkbak`
    - To avoid typing this every time you want to run the program,
you can alias the above command with: `alias mkbak='poetry run mkbak'`.

### From Source

- Download the repository:
  - `git clone https://github.com/sudo-julia/mkbak`
- Enter the repo
  - `cd mkbak`
- Build the package:
  - `python3 setup.py sdist bdist_wheel`
- Install from the local build
  - `pip install --user -U .`
- Run mkbak:
  - `mkbak`
  - Please note that running from a local build may not set up the entry point
correctly, resulting in: `bash: command not found: mkbak`. In this case, simply
run `alias mkbak='python3 -m mkbak'`. This sets up `mkbak` to be run as
a module when `mkbak` is typed, which solves the entry point problem.
You can add the `alias` command to the bottom of your shell's configuration file
for it to be set automatically at your terminal's initialization.

## Usage

```text
usage: mkbak [-h] [-a] [--ansi] [--bind BIND] [-d] [-e] [--height HEIGHT] [-i] [--no_mouse] [--no_recursion]
             [--no_sort] [--padding PADDING] [-p PATH] [--preview PREVIEW] [--print_query] [--prompt PROMPT]
             [-q QUERY] [-u] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -d, --delete          iterate through '.bak' files to delete
  -q QUERY, --query QUERY
                        start the finder with the given query
  -u, --unbak           restore files to their most recent backup
  --version             print version information

  -a, --all             show hidden and 'dot' files
  --ansi                enable processing of ANSI color codes
  --bind BIND           custom keybindings. refer to fzf's manpage
  -e, --exact           exact matching
  --height HEIGHT       display fzf window with the given height
  -i, --ignore_case     ignore case distinction
  --no_mouse            disable mouse interaction
  --no_recursion        run mkbak without recursing through subdirectories
  --no_sort             don't sort the results
  --padding PADDING     padding inside the menu's border
  -p PATH, --path PATH  directory to iterate through (default '.')
  --preview PREVIEW     starts external process with current line as arg
  --print_query         print query as the first line
  --prompt PROMPT       input prompt (default: '> ')
  -v, --verbose         explain what is being done
```

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

## TODO

- [X] Package for pypi
- [X] Define entry point so the program can be run as `mkbak`
- [X] Add all options to README
- [X] Github releases
- [X] Move argument parsing to a separate module
- [ ] Mode to replace a regular file with its backup
- [ ] Create documentation
- [ ] Shell completions

## Credits

Thanks to [junegunn](https://github.com/junegunn) for making [fzf](https://github.com/junegunn/fzf)

Thanks to [dahlia](https://github.com/dahlia) for making [iterfzf](https://github.com/dahlia/iterfzf)
