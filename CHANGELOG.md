# Changelog

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
