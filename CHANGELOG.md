## Changelog
`mkbak` follows semantic versioning, with the exception of the jump between 0.7.0 and 1.0.0

### Version 1.0.0
Released xx xxx, 2021

### Version 0.7.0
Released 23 Jan, 2021

- Added options `no_mouse`, `query`, `print_query` and `prompt` (all are calls to `iterfzf`)
- Uses the `rich` library to format messages output with the `-v|--verbose` flag
- Type hinting made more managable by upgraded `mypy` version and `__future__.annotations` for better backwards compatibility
