"""arguments for mkbak"""
from __future__ import annotations
import argparse
from typing import Any
from mkbak import VERSION  # type: ignore


def get_arguments() -> dict[str, Any]:
    """get the arguments"""
    # TODO option to provide files as arguments to backup
    # TODO option for recursion depth specification
    # TODO option to unbak a file (replace original with backup) [high priority]
    parser = argparse.ArgumentParser()
    main_args = parser.add_argument_group()
    mkbak_mode = parser.add_mutually_exclusive_group()

    main_args.add_argument(
        "-a", "--all", help="show hidden and 'dot' files", action="store_true"
    )
    main_args.add_argument(
        "--ansi",
        help="enable processing of ANSI color codes",
        action="store_true",
    )
    main_args.add_argument(
        "--bind",
        help="custom keybindings. refer to fzf's manpage",
        type=str,
    )
    mkbak_mode.add_argument(
        "-d",
        "--delete",
        help="iterate through '.bak' files to delete",
        action="store_true",
    )
    main_args.add_argument("-e", "--exact", help="exact matching", action="store_true")
    main_args.add_argument(
        "--height",
        help="display fzf window with the given height",
        type=int,
    )
    main_args.add_argument(
        "-i",
        "--ignore_case",
        help="ignore case distinction",
        action="store_true",
    )
    main_args.add_argument(
        "--no_mouse", help="disable mouse interaction", action="store_false"
    )
    main_args.add_argument(
        "--no_recursion",
        help="run mkbak without recursing through subdirectories",
        action="store_false",
    )
    main_args.add_argument(
        "--no_sort",
        help="don't sort the results",
        action="store_true",
    )
    main_args.add_argument(
        "--padding",
        help="padding inside the menu's border",
        type=int,
    )
    main_args.add_argument(
        "-p",
        "--path",
        default=".",
        help="directory to iterate through (default '.')",
        type=str,
    )
    main_args.add_argument(
        "--preview",
        default=None,
        help="starts external process with current line as arg",
        type=str,
    )
    main_args.add_argument(
        "--print_query", help="print query as the first line", action="store_true"
    )
    main_args.add_argument(
        "--prompt", default="> ", help="input prompt (default: '> ')", type=str
    )
    mkbak_mode.add_argument(
        "-q",
        "--query",
        default="",
        help="start the finder with the given query",
        type=str,
    )
    mkbak_mode.add_argument(
        "-u",
        "--unbak",
        help="restore files to their most recent backup",
        action="store_true",
    )
    main_args.add_argument(
        "-v", "--verbose", help="explain what is being done", action="store_true"
    )
    parser.add_argument(
        "--version",
        help="print version information",
        version=f"mkbak.py v{VERSION}",
        action="version",
    )

    return vars(parser.parse_args())
