#!/usr/bin/env python3
"""
iterate through files, feed them to 'iterfzf' for selection
and make backups of the chosen files
"""
import os
import shutil
import stat
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Generator, List, Optional
from iterfzf import iterfzf


# pylint: disable=fixme, unsubscriptable-object
# TODO remove unsubscriptable-object once pylint updates (currently broken on typing,
# see issue #3882)

__version__ = "v0.6.3"
# TODO move copied and errors to a local scope
copied: List[str] = []
errors: List[str] = []


def copy_all(file: str, location: str) -> bool:
    """copy a file owner and group intact"""
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


# TODO condense iteration to one function
def iterate_files(
    search_path: str, file_ext: Optional[str], find_hidden=False
) -> Generator[str, None, None]:
    """iterate through files as DirEntries to feed to fzf wrapper"""
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            try:
                if not find_hidden and entry.name.startswith("."):
                    pass
                elif file_ext and not entry.name.endswith(file_ext):
                    pass
                else:
                    yield entry.path
            except PermissionError:
                errors.append(f"Permission Denied: Unable to access '{entry}'")


def recursive(
    search_path: str, file_ext: Optional[str], find_hidden=None
) -> Generator[str, None, None]:
    """recursively yield DirEntries"""
    with os.scandir(search_path) as iterated:
        for entry in iterated:
            try:
                if not find_hidden and entry.name.startswith("."):
                    pass
                elif entry.is_dir(follow_symlinks=False):
                    yield from recursive(entry.path, FILETYPE, HIDDEN)
                elif file_ext and not entry.name.endswith(file_ext):
                    pass
                else:
                    yield entry.path
            except PermissionError:
                errors.append(f"Permission Denied: Unable to access '{entry}'")


def main():
    """parse args and launch the whole thing"""
    # TODO is there a way to store options in a tuple and unload them into
    #      both functions?
    # if the height option isn't present, fall back to the original 'iterfzf'
    try:
        if NO_RECURSE:
            files = iterfzf(
                iterable=(iterate_files(PATH, FILETYPE, HIDDEN)),
                case_sensitive=IGNORE,
                exact=EXACT,
                encoding="utf-8",
                height=HEIGHT,
                preview=PREVIEW,
                multi=True,
            )
        else:
            files = iterfzf(
                iterable=(recursive(PATH, FILETYPE, HIDDEN)),
                case_sensitive=IGNORE,
                exact=EXACT,
                encoding="utf-8",
                height=HEIGHT,
                preview=PREVIEW,
                multi=True,
            )
    except TypeError:
        if NO_RECURSE:
            files = iterfzf(
                iterable=(iterate_files(PATH, FILETYPE, HIDDEN)),
                case_sensitive=IGNORE,
                exact=EXACT,
                encoding="utf-8",
                preview=PREVIEW,
                multi=True,
            )
        else:
            files = iterfzf(
                iterable=(recursive(PATH, FILETYPE, HIDDEN)),
                case_sensitive=IGNORE,
                exact=EXACT,
                encoding="utf-8",
                preview=PREVIEW,
                multi=True,
            )

    if files:
        for file in files:
            try:
                location: str = f"{file}.bak"
                success = copy_all(file, location)
                if VERBOSE and success:
                    copied.append(f"{file} -> {location}")
            except TypeError:
                errors.append(f"Type Error: Unable to copy '{file}' to '{file}.bak'")

    verbose(copied, errors)


def verbose(files_copied: str, errors_thrown: str):
    """print information on file copies and errors"""
    if len(files_copied) > 0:
        print("Copied:")
        for file in files_copied:
            print(file)
    if len(errors_thrown) > 0:
        print("Errors:")
        for error in errors_thrown:
            print(error)


if __name__ == "__main__":
    # TODO option to provide files as arguments to backup
    # TODO option for recursion depth specification
    # TODO option to find by file or dir
    parser = ArgumentParser()
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
        "-v", "--verbose", help="explain what is being done", action="store_true"
    )
    parser.add_argument("--version", help="print version number", action="store_true")

    args = parser.parse_args()

    EXACT: bool = args.exact
    FILETYPE: Optional[str] = args.filetype
    # set height as a constant, using a oneliner if-else statement
    HEIGHT: str = str(args.height) + "%" if args.height in range(0, 101) else "100%"
    HIDDEN: bool = args.all
    IGNORE: bool = args.ignore_case
    # set the path as argument given, and expand '~' to "$HOME" if given
    PATH: str = args.path if args.path[0] != "~" else Path(args.path).expanduser()
    PREVIEW: Optional[str] = args.preview
    NO_RECURSE: bool = args.no_recurse
    VERBOSE: bool = args.verbose

    if args.version:
        print(f"mkbak.py {__version__}")
    else:
        main()

    sys.exit(0)
