from __future__ import annotations

from argparse import ArgumentParser, Namespace
import glob
import json
from pathlib import Path
import subprocess
import sys
from typing import cast

from packaging.requirements import Requirement

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


PROJECT_DIR = Path(__file__).parents[1]
DEFAULT_EXCLUDES: list[str] = []


def list_test_folders(exclude_folders: list[str] | None) -> int:
    """List all folders with tests"""
    exclude_folders = exclude_folders or []
    exclude_folders.extend(DEFAULT_EXCLUDES)
    res = 0
    for exclude in exclude_folders:
        if not (PROJECT_DIR / exclude).is_dir():
            print(f"'{exclude}' is not a valid folder")
            res = 1
    if res:
        return 1

    excludes = tuple(exclude_folders)
    test_folders = [
        folder.partition("/")[0]
        for folder in glob.glob("*/tests")
        if not folder.startswith(excludes)
    ]
    print(json.dumps(sorted(test_folders)))
    return 0


def install_local_requirements(name: str, installed_pkgs: set[str] | None = None) -> int:
    """Install local requirements recursively."""
    installed_pkgs = installed_pkgs or set()

    reqs_folder = PROJECT_DIR / name
    content = tomllib.loads(
        (reqs_folder / "pyproject.toml").read_text()
    )
    dependencies = [
        deps
        for req in content["project"].get("dependencies", [])
        if (deps := Requirement(req).name).startswith("standard-")
    ]
    for deps in dependencies:
        if deps in installed_pkgs:
            continue
        if install_local_requirements(deps.removeprefix("standard-"), installed_pkgs):
            return 1
    p = subprocess.run(["pip", "install", reqs_folder], stdout=sys.stdout, stderr=sys.stderr)
    return p.returncode


class ListTestFoldersArgs(Namespace):
    exclude: list[str] | None


class InstallLocalReqsArgs(Namespace):
    folder: str


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="Subcommands", required=True)

    parser_test_folders = subparsers.add_parser("list-test-folders")
    parser_test_folders.set_defaults(action="list-test-folders")
    parser_test_folders.add_argument(
        "--exclude",
        action="append",
        help="Root folders to exclude from search",
    )

    parser_local_reqs = subparsers.add_parser("install-local-requirements")
    parser_local_reqs.set_defaults(action="install-local-requirements")
    parser_local_reqs.add_argument(
        "folder",
        metavar="FOLDER",
        help="Current deadlib backport to install",
    )

    argv = argv or sys.argv[1:]
    args = parser.parse_args(argv)

    if args.action == "list-test-folders":
        args = cast(ListTestFoldersArgs, args)
        return list_test_folders(args.exclude)
    if args.action == "install-local-requirements":
        args = cast(InstallLocalReqsArgs, args)
        return install_local_requirements(args.folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
