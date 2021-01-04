#!/usr/bin/env python3
"""
iterate through files, feed them to 'iterfzf' for selection
and make backups of the chosen files
"""
import argparse
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Generator, Optional
from iterfzf import iterfzf


__version__ = "v0.5.1"
# pylint: disable=fixme, unsubscriptable-object
# TODO remove unsubscriptable-object once pylint updates (currently broken on typing,
# see issue #3882)
# TODO put iterators in a class


def copy_all(file: str, location: str):
    """copy a file owner and group intact"""
    # function from https://stackoverflow.com/a/43761127 (thank you mayra!)
    # copy content, stat-info, mode and timestamps
    try:
        shutil.copytree(file, location)
    except NotADirectoryError:
        shutil.copy2(file, location)
    # copy owner and group
    finally:
        owner_group = os.stat(file)
        os.chown(location, owner_group[stat.ST_UID], owner_group[stat.ST_GID])


def iterate_files(
    search_path: str, file_ext: Optional[str], find_hidden=False
) -> Generator[str, None, None]:
    """iterate through files as DirEntries to feed to fzf wrapper"""
    with os.scandir(search_path) as iterated:
        if file_ext:
            for entry in iterated:
                if not find_hidden and entry.name.startswith("."):
                    pass
                else:
                    if entry.name.endswith(file_ext):
                        try:
                            yield entry.path
                        except PermissionError:
                            pass
        elif not file_ext:
            for entry in iterated:
                if not find_hidden and entry.name.startswith("."):
                    pass
                else:
                    try:
                        yield entry.path
                    except PermissionError:
                        pass


def main():
    """:"""
    # TODO is there a way to store options in a tuple and unload them into
    #      both functions?
    try:
        if no_recurse:
            files = iterfzf(
                iterable=(iterate_files(path, filetype, hidden)),
                case_sensitive=ignore,
                exact=exact,
                encoding="utf-8",
                height=HEIGHT,
                preview=preview,
                multi=True,
            )
        else:
            files = iterfzf(
                iterable=(recursive(path, hidden)),
                case_sensitive=ignore,
                exact=exact,
                encoding="utf-8",
                height=HEIGHT,
                preview=preview,
                multi=True,
            )
    except TypeError:
        if no_recurse:
            files = iterfzf(
                iterable=(iterate_files(path, filetype, hidden)),
                case_sensitive=ignore,
                exact=exact,
                encoding="utf-8",
                preview=preview,
                multi=True,
            )
        else:
            files = iterfzf(
                iterable=(recursive(path, hidden)),
                case_sensitive=ignore,
                exact=exact,
                encoding="utf-8",
                preview=preview,
                multi=True,
            )

    try:
        for file in files:
            location = f"{file}.bak"
            copy_all(file, location)
            if verbose:
                print(f"{file} -> {location}")
    except TypeError:
        pass


def recursive(search_path: str, find_hidden=None) -> Generator[str, None, None]:
    """recursively yield DirEntries"""
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            if not find_hidden and entry.name.startswith("."):
                pass
            else:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        yield from recursive(entry.path, hidden)
                    else:
                        yield entry.path
                except PermissionError:
                    pass


if __name__ == "__main__":
    # TODO argument to give a file or list of files and back those up
    # TODO make extension copying recursive
    # TODO arg addition to recursive that allows for depth to recurse
    # TODO option to find by file or dir
    parser = argparse.ArgumentParser()
    main_args = parser.add_argument_group()
    matching_group = parser.add_mutually_exclusive_group()

    main_args.add_argument(
        "-a", "--all", help="show hidden and 'dot' files.", action="store_true"
    )
    matching_group.add_argument(
        "-e", "--exact", help="exact matching.", action="store_true"
    )
    matching_group.add_argument(
        "-f",
        "--filetype",
        default=None,
        help="only find files of a provided extension. recursion not supported.",
        type=str,
    )
    main_args.add_argument(
        "--height",
        default=100,
        help="""display fzf window with the given height. takes an
                           int between 0-100.""",
        type=int,
    )
    matching_group.add_argument(
        "-i",
        "--ignore_case",
        help="ignore case distinction.",
        action="store_true",
    )
    main_args.add_argument(
        "-p",
        "--path",
        help="directory to iterate through (default './')",
        default=".",
        type=str,
    )
    main_args.add_argument(
        "--preview",
        default=None,
        help="starts external process with current line as arg.",
        type=str,
    )
    main_args.add_argument(
        "--no_recurse",
        help="run mkbak in the current dir only (no recursion)",
        action="store_true",
    )
    main_args.add_argument(
        "-v", "--verbose", help="print file file created", action="store_true"
    )
    parser.add_argument("--version", help="print version number", action="store_true")

    args = parser.parse_args()

    exact: bool = args.exact
    filetype: Optional[str] = args.filetype
    # set height as a constant, using a oneliner if-else statement
    HEIGHT: str = str(args.height) + "%" if args.height in range(0, 101) else "100%"
    hidden: bool = args.all
    ignore: bool = args.ignore_case
    # set the path as argument given, and expand '~' to "$HOME" if given
    path: str = args.path if args.path[0] != "~" else Path(args.path).expanduser()
    preview: Optional[str] = args.preview
    no_recurse: bool = args.no_recurse
    verbose: bool = args.verbose

    if args.version:
        print(f"mkbak.py {__version__}")
        sys.exit(0)

    main()
    sys.exit(0)
