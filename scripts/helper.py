from pathlib import Path
import os
import tomllib

from packaging.requirements import Requirement

script_dir = os.path.dirname(__file__)
project_dir = script_dir.rsplit("/", 1)[0]


def local_dependency_names(name) -> [str]:
    content = tomllib.loads(Path(f"{project_dir}/{name}/pyproject.toml").read_text())
    dependencies = [
        Requirement(s).name for s in content["project"].get("dependencies", [])
    ]
    local_names = [
        name.partition("standard-")[2]
        for name in dependencies
        if name.startswith("standard-")
    ]
    collected_names = [local_dependency_names(name) + [name] for name in local_names]
    # NOTE: Do not sort the collection. The order is important
    return [name for names in collected_names for name in names]


if __name__ == "__main__":
    import sys

    try:
        name = sys.argv[1]
    except IndexError:
        name = os.path.basename(os.getcwd())
    for name in local_dependency_names(name):
        print(name)
