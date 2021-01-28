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
from mkbak_iterfzf import iterfzf
from rich import box
from rich.panel import Panel
from rich import print as rich_print
from mkbak import version


# pylint: disable=fixme

copied: list[str] = []
errors: list[str] = []


def iterate_files(
    search_path: str, recursion: bool, find_hidden: bool = False
) -> Generator[str, None, None]:
    """
    iterate through files as DirEntries to feed to fzf wrapper
    """
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            try:
                if not find_hidden and entry.name.startswith("."):
                    pass
                elif recursion and entry.is_dir(follow_symlinks=False):
                    yield from iterate_files(entry.path, recursion, find_hidden)
                else:
                    yield entry.path
            except PermissionError:
                errors.append(f"Permission Denied: Unable to access '{entry}'")


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


def main():
    """parse args and launch the whole thing"""
    # TODO option to provide files as arguments to backup
    # TODO option for recursion depth specification
    # TODO option to delete .bak files

    # TODO move these to a function that gets args for main
    parser = ArgumentParser()
    main_args = parser.add_argument_group()
    matching_group = parser.add_mutually_exclusive_group()

    main_args.add_argument(
        "-a", "--all", help="show hidden and 'dot' files", action="store_true"
    )
    matching_group.add_argument(
        "-e", "--exact", help="exact matching", action="store_true"
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
        "--no_recursion",
        help="run mkbak without recursing through subdirectories",
        action="store_false",
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
        "--version",
        help="print version information",
        version=f"mkbak.py {version}",
        action="version",
    )

    args = parser.parse_args()

    exact: bool = args.exact
    # set height as a constant, using a oneliner if-else statement
    height: str = f"{args.height}%" if args.height in range(0, 100) else "100%"
    hidden: bool = args.all
    ignore: bool = args.ignore_case
    mouse: bool = args.no_mouse
    recursion: bool = args.no_recursion
    # set the path as argument given, and expand '~' to "$HOME" if given
    path: str = args.path if args.path[0] != "~" else str(Path(args.path).expanduser())
    preview: str | None = args.preview
    print_query: bool = args.print_query
    prompt: str = args.prompt
    query: str = args.query
    verbose: bool = args.verbose

    try:
        files: list[str] | None = iterfzf(
            iterable=(iterate_files(path, recursion, hidden)),
            case_sensitive=ignore,
            exact=exact,
            encoding="utf-8",
            height=height,
            query=query,
            preview=preview,
            print_query=print_query,
            prompt=prompt,
            mouse=mouse,
            multi=True,
        )
    except PermissionError:
        errors.append(f"PermissionError: Unable to access '{path}'")
        print_verbose(copied, errors)
        sys.exit(13)

    # if files exist, copy them
    if files and files[0] != "":
        for file in files:
            if file is None:  # this catches None being given as a file by --print_query
                sys.exit(130)
            try:
                location: str = f"{file}.bak"
                success: bool = copy_all(file, location)
                if verbose and success:
                    copied.append(f"{file} -> {location}")
            except TypeError:
                errors.append(f"Type Error: Unable to copy '{file}' to '{file}.bak'")
    else:
        sys.exit(130)

    print_verbose(copied, errors)
    return 0


def print_verbose(files_copied: list[str] | str, errors_thrown: list[str] | str):
    """print information on file copies and errors"""
    if files_copied:
        files_copied = "\n".join(files_copied)
        rich_print(
            Panel.fit(
                f"[green]{files_copied}",
                title="Files Copied",
                box=box.SQUARE,
            )
        )
    if errors_thrown:
        if files_copied:
            print()
        errors_thrown = "\n".join(errors_thrown)
        rich_print(
            Panel.fit(
                f"[red]{errors_thrown}",
                title="Errors",
                box=box.SQUARE,
            )
        )


if __name__ == "__main__":
    main()
    sys.exit(0)
