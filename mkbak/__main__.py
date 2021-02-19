#!/usr/bin/env python3
from __future__ import annotations
import filecmp
import errno
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Any, Generator
from mkbak_iterfzf import iterfzf
from rich import box
from rich.panel import Panel
from rich.prompt import Confirm
from rich import print as rich_print
from mkbak import copied, deleted, errors, warnings
from mkbak.mkbak_args import get_arguments


# TODO find a way to break this up
def iterate_files(
    search_path: str,
    recursion: bool,
    delete: bool,
    find_hidden: bool = False,
) -> Generator[str, None, None]:
    """
    iterate through files to provide to iterfzf
    """
    try:
        with os.scandir(search_path) as iterated:
            for entry in iterated:
                try:
                    if not find_hidden:
                        if entry.name.startswith("."):
                            continue
                    if not delete:
                        if entry.name.endswith(".bak"):
                            continue
                    else:
                        if not entry.name.endswith(".bak"):
                            continue
                        yield entry.path
                    if recursion and entry.is_dir(follow_symlinks=False):
                        yield from iterate_files(
                            entry.path, recursion, delete, find_hidden
                        )
                except PermissionError:
                    if entry.is_dir(follow_symlinks=False):
                        errors.append(f"Unable to access directory '{entry.path}'.")
                    else:
                        errors.append(f"Unable to access file '{entry.path}'.")
                yield entry.path
    except FileNotFoundError:
        errors.append(f"Can't search '{search_path}', as it doesn't exist.")
        print_verbose(copied, deleted, errors, warnings)
        sys.exit(130)


def copy_all(files: list[str], verbosity: bool):
    """copy a file, leaving the owner and group intact"""
    # function from https://stackoverflow.com/a/43761127 (thank you mayra!)
    # copy content, stat-info, mode and timestamps
    copy_success: bool = False

    for file in files:
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
                    warnings.append(f"'{location}' not overwritten.")
                    continue

        try:
            shutil.copy2(file, location)  # copy file
            owner_group = os.stat(file)  # copy owner and group
            os.chown(location, owner_group[stat.ST_UID], owner_group[stat.ST_GID])
            copy_success = True
        except IsADirectoryError:
            # TODO work out skipping directories or a separate copy for them
            warnings.append(f"Couldn't copy directory '{file}'.")
        except PermissionError as perm_err:
            # error thrown if no read permissions
            if perm_err.errno == errno.EACCES:
                errors.append(f"Can't access '{file}'. Do you have read permissions?")
            # error thrown if ownership can't be changed
            else:
                if Path(location).exists():
                    # the backup was made, but permissions were unable to be changed
                    warnings.append(
                        f"'{location}' was copied, but ownership couldn't be changed."
                    )
                    copy_success = True
                else:
                    errors.append(f"Unable to back up '{file}'.")
        if copy_success and verbosity:
            copied.append(f"{file} -> {location}")


# TODO confirm option|option to confirm number of files to delete
#      -- functionally similar to rm -i|-I
def delete_backups(files: list[str], verbosity: bool):
    """delete files"""
    for file in files:
        try:
            os.remove(file)
            if verbosity:
                deleted.append(f"'{file}'")
        except PermissionError as perm_err:
            if perm_err.errno == errno.EACCES:
                parent = Path(file).parent
                errors.append(
                    f"Couldn't delete '{file}'. Do you have write access to '{parent}'?"
                )
            else:
                errors.append(f"Unable to delete '{file}'.")


def main():
    """parse args and launch the whole thing"""
    args: dict[str, Any] = get_arguments()

    # set height if valid
    if args["height"] in range(0, 100):
        args["height"] = f"{args['height']}%"
    # set the case-sensitive option in accordance to iterfzf's options
    # (None for smartcase, False for case-insensitivity)
    if args["ignore_case"]:
        args["ignore_case"] = False
    else:
        args["ignore_case"] = None
    # s
    if args["padding"] in range(0, 50):
        args["padding"] = f"{args['padding']}%"
    # set the path as argument given, and expand '~' to "$HOME" if given
    if args["path"][0] == "~":
        args["path"] = str(Path(args["path"]).expanduser())
    # set prompt to default unless in 'delete' mode
    if args["delete"]:
        args["prompt"] = "rm > "

    try:
        files = iterfzf(
            iterable=(
                iterate_files(
                    args["path"], args["no_recursion"], args["delete"], args["all"]
                )
            ),
            ansi=args["ansi"],
            bind=args["bind"],
            case_sensitive=args["ignore_case"],
            exact=args["exact"],
            encoding="utf-8",
            height=args["height"],
            query=args["query"],
            padding=args["padding"],
            preview=args["preview"],
            print_query=args["print_query"],
            prompt=args["prompt"],
            no_sort=args["no_sort"],
            mouse=args["no_mouse"],
            multi=True,
        )
    except PermissionError:
        errors.append(
            f"Unable to access '{args['path']}'. Do you have read/execute permissions?"
        )
        print_verbose(copied, deleted, errors, warnings)
        sys.exit(13)

    if files and files[0] != "":
        if args["delete"]:
            delete_backups(files, args["verbose"])
        else:
            copy_all(files, args["verbose"])
    else:
        sys.exit(130)

    print_verbose(copied, deleted, errors, warnings)
    return 0


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
