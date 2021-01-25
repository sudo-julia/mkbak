#!/usr/bin/env python3
"""
iterate through files, feed them to 'iterfzf' for selection
and make backups of the chosen files
"""
from __future__ import annotations
import os
import shutil
import stat
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Generator
from iterfzf import iterfzf
from rich import box
from rich.panel import Panel
from rich import print as rprint


# pylint: disable=fixme, unsubscriptable-object
# TODO remove unsubscriptable-object once pylint updates (currently broken on typing,
# see issue #3882)

__version__ = "v0.7.1"
copied: list[str] = []
errors: list[str] = []


def copy_all(file: str, location: str) -> bool:
    """copy a file, leaving the owner and group intact"""
    # function from https://stackoverflow.com/a/43761127 (thank you mayra!)
    # copy content, stat-info, mode and timestamps
    try:
        if Path(file).is_dir():
            shutil.copytree(file, location)
        elif Path(file).is_file():
            shutil.copy2(file, location)
        # copy owner and group
        owner_group = os.stat(file)
        os.chown(location, owner_group[stat.ST_UID], owner_group[stat.ST_GID])
        return True
    except PermissionError:
        errors.append(f"Permission Denied: Unable to access '{file}'")
        return False


def iterate_files(
    search_path: str, file_ext: str | None, find_hidden=False
) -> Generator[str, None, None]:
    """
    iterate through files as DirEntries to feed to fzf wrapper - recursion optional
    """
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            try:
                if not find_hidden and entry.name.startswith("."):
                    pass
                elif not NO_RECURSE and entry.is_dir(follow_symlinks=False):
                    yield from iterate_files(entry.path, FILETYPE, HIDDEN)
                elif file_ext and not entry.name.endswith(file_ext):
                    pass
                else:
                    yield entry.path
            except PermissionError:
                errors.append(f"Permission Denied: Unable to access '{entry}'")


def main():
    """parse args and launch the whole thing"""
    # if the height option isn't present, fall back to the original 'iterfzf'
    try:
        files: list | None = iterfzf(
            iterable=(iterate_files(PATH, FILETYPE, HIDDEN)),
            case_sensitive=IGNORE,
            exact=EXACT,
            encoding="utf-8",
            height=HEIGHT,
            query=QUERY,
            preview=PREVIEW,
            print_query=PRINT_QUERY,
            prompt=PROMPT,
            mouse=MOUSE,
            multi=True,
        )
    except TypeError:
        files: list | None = iterfzf(
            iterable=(iterate_files(PATH, FILETYPE, HIDDEN)),
            case_sensitive=IGNORE,
            exact=EXACT,
            encoding="utf-8",
            query=QUERY,
            preview=PREVIEW,
            print_query=PRINT_QUERY,
            prompt=PROMPT,
            mouse=MOUSE,
            multi=True,
        )
    except PermissionError:
        errors.append(f"PermissionError: Unable to access '{PATH}'")
        verbose(copied, errors)
        sys.exit(13)

    # if files exist, copy them
    if files and files[0] != "":
        for file in files:
            if file is None:  # this catches None being given as a file by --print_query
                sys.exit(130)
            try:
                location: str = f"{file}.bak"
                success: bool = copy_all(file, location)
                if VERBOSE and success:
                    copied.append(f"{file} -> {location}")
            except TypeError:
                errors.append(f"Type Error: Unable to copy '{file}' to '{file}.bak'")
    else:
        sys.exit(130)

    verbose(copied, errors)


def verbose(files_copied: list[str], errors_thrown: list[str]):
    """print information on file copies and errors"""
    if len(files_copied) > 0:
        files_copied = "\n".join(files_copied)
        rprint(
            Panel(
                f"[green]{files_copied}",
                title="Files Copied",
                box=box.SQUARE,
                expand=False,
                highlight=True,
            )
        )
    if len(errors_thrown) > 0:
        if len(files_copied) > 0:
            print()
        errors_thrown = "\n".join(errors_thrown)
        rprint(
            Panel(
                f"[red]{errors_thrown}",
                title="Errors",
                box=box.SQUARE,
                expand=False,
                highlight=True,
            )
        )


if __name__ == "__main__":
    # TODO option to provide files as arguments to backup
    # TODO option for recursion depth specification
    parser = ArgumentParser()
    main_args = parser.add_argument_group()
    matching_group = parser.add_mutually_exclusive_group()

    main_args.add_argument(
        "-a", "--all", help="show hidden and 'dot' files", action="store_true"
    )
    matching_group.add_argument(
        "-e", "--exact", help="exact matching", action="store_true"
    )
    matching_group.add_argument(
        "-f",
        "--filetype",
        default=None,
        help="find files of a provided extension",
        type=str,
    )
    main_args.add_argument(
        "--height",
        default=100,
        help="display fzf window with the given height",
        type=int,
    )
    main_args.add_argument(
        "-i",
        "--ignore_case",
        help="ignore case distinction",
        action="store_false",
    )
    main_args.add_argument(
        "--no_mouse", help="disable mouse interaction", action="store_false"
    )
    main_args.add_argument(
        "--no_recurse",
        help="run mkbak without recursing through subdirectories",
        action="store_true",
    )
    main_args.add_argument(
        "-p",
        "--path",
        default=".",
        help="directory to iterate through (default './')",
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
    matching_group.add_argument(
        "-q",
        "--query",
        default="",
        help="start the finder with the given query",
        type=str,
    )
    main_args.add_argument(
        "-v", "--verbose", help="explain what is being done", action="store_true"
    )
    parser.add_argument(
        "--version", help="print version information", action="store_true"
    )

    args = parser.parse_args()

    if args.version:
        print(f"mkbak.py {__version__}")
        sys.exit(0)

    EXACT: bool = args.exact
    FILETYPE: str | None = args.filetype
    # set height as a constant, using a oneliner if-else statement
    HEIGHT: str = f"{args.height}%" if args.height in range(0, 101) else "100%"
    HIDDEN: bool = args.all
    IGNORE: bool = args.ignore_case
    MOUSE: bool = args.no_mouse
    NO_RECURSE: bool = args.no_recurse
    # set the path as argument given, and expand '~' to "$HOME" if given
    PATH: str = args.path if args.path[0] != "~" else Path(args.path).expanduser()
    PREVIEW: str | None = args.preview
    PRINT_QUERY: bool = args.print_query
    PROMPT: str = args.prompt
    QUERY: str = args.query
    VERBOSE: bool = args.verbose

    main()
    sys.exit(0)
