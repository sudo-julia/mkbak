## Changelog
`mkbak` follows semantic versioning  

### Version 0.7.0
Released on 23 Jan, 2021

  - Added options `no_mouse`, `query`, `print_query` and `prompt` (all are calls to `iterfzf`)
  - Uses the `rich` library to format messages output with the `-v|--verbose` flag
  - Type hinting made more managable by upgraded `mypy` version and `__future__.annotations` for better backwards compatibility
