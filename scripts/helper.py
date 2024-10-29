from pathlib import Path
import tomllib

from packaging.requirements import Requirement

def get_deadlib_names() -> None:
    content = tomllib.loads(Path("pyproject.toml").read_text())
    dependencies = [
        Requirement(s).name for s in content["project"].get("dependencies", [])
    ]
    names = [
        name.partition("standard-")[2]
        for name in dependencies if name.startswith("standard-")
    ]
    for name in names:
        print(name)


if __name__ == "__main__":
    get_deadlib_names()
