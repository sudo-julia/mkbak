#!/usr/bin/env python3
"""
make backups of files selected by mkbak-iterfzf
"""
from __future__ import annotations
import filecmp
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
from rich.prompt import Confirm
from rich import print as rich_print
from mkbak import version


copied: list[str] = []
deleted: list[str] = []
errors: list[str] = []
warnings: list[str] = []


def iterate_files(
    search_path: str, recursion: bool, delete: bool, find_hidden: bool = False
) -> Generator[str, None, None]:
    """
    iterate through files to provide to iterfzf
    """
    if not Path(search_path).exists():
        errors.append(f"'{search_path}' does not exist")
        print_verbose(copied, deleted, errors, warnings)
        sys.exit(130)
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            try:
                if not find_hidden and entry.name.startswith("."):  # pass hidden files
                    pass
                elif recursion and entry.is_dir(follow_symlinks=False):
                    yield from iterate_files(entry.path, recursion, delete, find_hidden)
                elif entry.name.endswith(".bak"):
                    if delete:
                        yield entry.path
                elif delete:
                    pass
                else:
                    yield entry.path
            except PermissionError:
                errors.append(f"Permission Denied: Unable to access '{entry}'")


def copy_all(files: list[str], verbosity: bool):
    """copy a file, leaving the owner and group intact"""
    # function from https://stackoverflow.com/a/43761127 (thank you mayra!)
    # copy content, stat-info, mode and timestamps
    copy_success: bool

    for file in files:
        if file is None:
            sys.exit(130)

        location = f"{file}.bak"
        # operations for if the backup file already exists
        if Path(location).exists():
            # if the files are the same, do not copy
            if filecmp.cmp(file, location, shallow=True):
                copied.append(f"{location} is already up to date.")
                continue
            # if the location to copy to has been modified more recently than the
            # original file, give the option to overwrite it
            if Path(location).stat().st_mtime > Path(file).stat().st_mtime:
                overwrite = Confirm.ask(
                    f"'{location}' exists/is newer than '{file}'. Copy anyway? ",
                )
                if not overwrite:
                    warnings.append(f"'{location}' not overwritten")
                    continue

        try:
            shutil.copy2(file, location)
            # copy owner and group
            owner_group = os.stat(file)
            os.chown(location, owner_group[stat.ST_UID], owner_group[stat.ST_GID])
            copy_success = True
        except PermissionError:
            errors.append(f"Permission Denied: Unable to back up '{file}'")
            copy_success = False
        if copy_success and verbosity:
            copied.append(f"{file} -> {location}")


# TODO confirm option|option to confirm number of files to delete
#      -- functionally similar to rm -i|-I
def delete_backups(files: list[str], verbosity: bool):
    """delete files"""
    for file in files:
        if file is None:
            sys.exit(130)
        try:
            os.remove(file)
            if verbosity:
                deleted.append(f"'{file}'")
        except PermissionError:
            errors.append(f"Permission Denied: Unable to delete '{file}'")
        except FileNotFoundError:
            errors.append(f"File Not Found: '{file}' does not exist")


def main():
    """parse args and launch the whole thing"""
    # TODO option to provide files as arguments to backup
    # TODO option for recursion depth specification
    # TODO option to unbak a file (replace original with backup)
    parser = ArgumentParser()
    main_args = parser.add_argument_group()
    matching_group = parser.add_mutually_exclusive_group()

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
    matching_group.add_argument(
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
        help="do not sort the results",
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

    ansi: bool = args.ansi
    bind: str | None = args.bind
    delete: bool = args.delete
    exact: bool = args.exact
    # set height as a constant, using a oneliner if-else statement
    height: str | None = f"{args.height}%" if args.height in range(0, 100) else None
    hidden: bool = args.all
    # set the case-sensitive option in accordance to iterfzf's options
    # (None for smartcase, False for case-insensitivity
    ignore: bool | None = False if args.ignore_case else None
    mouse: bool = args.no_mouse
    padding: str | None = f"{args.padding}%" if args.padding in range(0, 50) else None
    # set the path as argument given, and expand '~' to "$HOME" if given
    path: str = args.path if args.path[0] != "~" else str(Path(args.path).expanduser())
    preview: str | None = args.preview
    print_query: bool = args.print_query
    # set prompt to default unless in 'delete' mode
    prompt: str = args.prompt if not args.delete else "rm > "
    query: str = args.query
    recursion: bool = args.no_recursion
    sort: bool = args.no_sort
    verbose: bool = args.verbose

    try:
        files: list[str] | None = iterfzf(
            iterable=(iterate_files(path, recursion, delete, hidden)),
            ansi=ansi,
            bind=bind,
            case_sensitive=ignore,
            exact=exact,
            encoding="utf-8",
            height=height,
            query=query,
            padding=padding,
            preview=preview,
            print_query=print_query,
            prompt=prompt,
            no_sort=sort,
            mouse=mouse,
            multi=True,
        )
    except PermissionError:
        errors.append(f"PermissionError: Unable to access '{path}'")
        print_verbose(copied, deleted, errors, warnings)
        sys.exit(13)

    if delete and files and files[0] != "":
        delete_backups(files, verbose)
    # if files exist, copy them
    elif files and files[0] != "":
        copy_all(files, verbose)
    else:
        sys.exit(130)

    print_verbose(copied, deleted, errors, warnings)


def print_verbose(
    files_copied: list[str] | str,
    files_deleted: list[str] | str,
    errors_thrown: list[str] | str,
    warnings_given: list[str] | str,
):
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
    elif files_deleted:
        files_deleted = "\n".join(files_deleted)
        rich_print(
            Panel.fit(
                f"[dark_orange]{files_deleted}",
                title="Files Deleted",
                box=box.SQUARE,
            )
        )
    if warnings_given:
        if files_copied or files_deleted:
            print()
        warnings_given = "\n".join(warnings_given)
        rich_print(
            Panel.fit(
                f"[orange1]{warnings_given}",
                title="Warnings",
                box=box.SQUARE,
            )
        )
    if errors_thrown:
        if files_copied or files_deleted or warnings_given:
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
