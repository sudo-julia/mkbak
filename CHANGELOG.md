# Changelog

`mkbak` follows semantic versioning, with the exception of the jump between
0.7.0 and 1.0.0

## Version 1.1.0

Released 2021-XX-XX

- `-d|--delete` option added
  - the `--delete` flag scans for '.bak' files in the current directory,
and instead of backing them up again, deletes them
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
