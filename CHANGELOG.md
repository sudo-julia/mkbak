# Changelog

## Version 1.3.0

Released 2021-03-01

- Progress bar added when copying or deleting files
- Removed excessive indentation
- Opening of directory to search switched to older open/close to remove another
level of indentation
- Argument handling moved to `mkbak_args`

- Bugfixes
  - `--no_sort` now works
  - Better value-checking with `--height` and `--padding`

## Version 1.2.2

Released 2021-02-19

- Global variable initialization moved to `__init__.py`
- Project structure changed
  - .pyi files added
  - py.typed files added
  - Argument parsing moved to module
  - Arguments stored as a dictionary (as opposed to argparse's Namespace object)
for consistency in setting variables. Previously, some values would be renamed
and some would be passed to `iterfzf` as is, but the dictionary allows values to
be changed in place

- Bugfixes
  - IsADirectoryError is now handled within mkbak

## Version 1.2.1

Released 2021-02-12

- Errors are more verbose, suggest fixes based off of error handling and have
a more human syntax
- Bugfixes
  - Previously when the user had read permission to a file, but no ownership,
the file was copied, but an error was thrown saying that access was denied.
`mkbak` will now detect during which stage of copying the file an error occurred,
and inform the user accordingly.

## Version 1.2.0

Released 2021-02-09

- `mkbak_iterfzf` version upgrade
- Added `ansi` option
- Added `bind` option
- Added `no_sort` option
- Added `padding` option

## Version 1.1.2

Released 2021-02-08

- if `foo.bak` already exists, `mkbak` will check:
  - if `foo` and `foo.bak`
are identical before making the backup, saving time copying files that are
already up to date
  - if `foo.bak` is more recently modified than `foo`, and give the option to
overwrite `foo.bak` accordingly

- smart case matching is now the default. `-i|--ignore_case` still provides
fully case-insensitive matching

- "Warnings" box added to display any issues that don't quite qualify as errors

## Version 1.1.1

Released 2021-02-03

- `--delete` option now acts recursively

## Version 1.1.0

Released 2021-02-03

- `-d|--delete` option added
  - the `--delete` flag scans for '.bak' files in the current directory,
and instead of backing them up again, deletes them
- default prompts changed for 'backup' and 'remove modes'
  - passing a `--prompt` argument will override the default
- '.bak' files are now passed over during iteration, removing the possibility of
creating '.bak.bak.bak...' files
- Errors are slightly more verbose

## Version 1.0.3

Released 2021-01-28

- `mkbak` can now be run without being called as a module!
- Some variables renamed to be more sensible

## Version 1.0.2

Released 2021-01-27

- Call `mkbak_iterfzf` so everyone has access to `--height` :)

## Version 1.0.1

Released 2021-01-28

- `mkbak` is now ready to roll on PyPi

## Version 0.7.0

Released 2020-01-23

- Added options `no_mouse`, `query`, `print_query` and `prompt`
(all are calls to `iterfzf`)
- Uses the `rich` library to format messages output with the `-v|--verbose` flag
- Type hinting made more managable by upgraded `mypy` version and
`__future__.annotations` for better backwards compatibility, allowing usage with
Python3.7>=
