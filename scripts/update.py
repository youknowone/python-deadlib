import os
import shutil


CPYTHON_SRC = os.environ["CPYTHON_SRC"]

ALL_NAMES = [
    "aifc",
    # "asynchat",  # removed in 3.12
    # "asyncore",  # removed in 3.12
    "cgi",
    "cgitb",
    "chunk",
    "crypt",
    "distutils",  # removed in 3.10
    "imghdr",
    "mailcap",
    # "msilib",  # cmodule _msi
    "nntplib",
    # "nis",  # cmodule
    # "ossaudiodev",  # cmodule
    "pipes",
    # "smtpd",  # removed in 3.12
    "sndhdr",
    # "spwd",  # cmodule
    "sunau",
    "telnetlib",
    "uu",
    "xdrlib",
]

ADDITIONAL_RESOURCES = {
    "nntplib": [
        # ("Lib/test/keycert3.pem", "tests/"),  # 3.10
        ("Lib/test/certdata/keycert3.pem", "tests/certdata/"),  # 3.11
    ],
}

LAST_RELEASES = {
    "3.5": "3.5.10",
    "3.6": "3.6.15",
    "3.7": "3.7.17",
    "3.8": "3.8.19",
    "3.9": "3.9.19",
    "3.10": "3.10.14",
    "3.11": "3.11.9",
    "3.12": "3.12.2",
}


def create(name):
    if os.path.exists(name):
        raise ValueError(f"{name} already exists")
    shutil.copytree("template", name)
    update_pyproject(name, "{version}")


def delete(name):
    shutil.rmtree(name)


def init(name):
    try:
        create(name)
    except OSError:
        delete(name)
        raise


def update_pyproject(name, version):
    pyproject_template = open("template/pyproject.toml").read()
    pyproject = pyproject_template
    pyproject = pyproject.replace("{name}", name)
    pyproject = pyproject.replace("{version}", version)
    assert pyproject != pyproject_template
    open(f"{name}/pyproject.toml", "w").write(pyproject)


def remove_package(name):
    if os.path.exists(f"{name}/{name}"):
        shutil.rmtree(f"{name}/{name}")  # dir package
    if os.path.exists(f"{name}/{name}.py"):
        os.remove(f"{name}/{name}.py")  # single file package


def update(name, version):
    version = LAST_RELEASES.get(version, version)
    has_py = os.path.exists(f"{CPYTHON_SRC}/Lib/{name}.py")
    has_dir = os.path.exists(f"{CPYTHON_SRC}/Lib/{name}")

    if has_py == has_dir:
        if has_py:
            raise ValueError(f"both {name} and {name}.py found in cpython source")
        else:
            raise ValueError(f"neither {name} found in cpython source")

    update_pyproject(name, version)

    cwd = os.getcwd()
    try:
        os.chdir(CPYTHON_SRC)
        os.system(f"git checkout v{version}")
    finally:
        os.chdir(cwd)

    remove_package(name)

    try:
        if has_py:
            # shutil.copy(f"{CPYTHON_SRC}/Lib/{name}.py", f"{name}/src/{name}.py")
            try:
                os.mkdir(f"{name}/{name}")
            except OSError:
                pass
            shutil.copy(f"{CPYTHON_SRC}/Lib/{name}.py", f"{name}/{name}/__init__.py")
        if has_dir:
            shutil.copytree(f"{CPYTHON_SRC}/Lib/{name}", f"{name}/{name}")
        if name != "chunk":
            shutil.copy(
                f"{CPYTHON_SRC}/Lib/test/test_{name}.py", f"{name}/tests/test_{name}.py"
            )
        shutil.copy(f"{CPYTHON_SRC}/Doc/library/{name}.rst", f"{name}/Doc/{name}.rst")

        for src, dst in ADDITIONAL_RESOURCES.get(name, []):
            if dst.endswith("/"):
                os.makedirs(f"{name}/{dst}", exist_ok=True)
            shutil.copy(f"{CPYTHON_SRC}/{src}", f"{name}/{dst}")
    except Exception:
        remove_package(name)
        raise


def run_test(name, version):
    PYENV_ROOT = os.environ["PYENV_ROOT"]

    minor_version = LAST_RELEASES[version]

    lib_path = f"{PYENV_ROOT}/versions/{minor_version}/lib/python{version}/{name}"
    if not os.path.exists(lib_path):
        lib_path += ".py"

    cwd = os.getcwd()
    try:
        if lib_path.endswith(".py"):
            os.remove(lib_path)
        else:
            shutil.rmtree(lib_path)
        os.chdir(name)
        os.putenv("PYTHONPATH", f"{os.getcwd()}/src")
        r = os.system(
            f"{PYENV_ROOT}/versions/{minor_version}/bin/python -m unittest tests/test_{name}.py"
        )
        assert r == 0, r
    finally:
        os.chdir(cwd)
        if lib_path.endswith(".py"):
            shutil.copy(f"{name}/{name}/__init__.py", lib_path)
        else:
            shutil.copytree(f"{name}/{name}", lib_path)
        os.unsetenv("PYTHONPATH")


def build_package(name):
    cwd = os.getcwd()
    try:
        os.chdir(name)
        r = os.system("python -m build")
        assert r == 0, r
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    import sys

    module_name = sys.argv[1]
    version = sys.argv[2]

    def action(module_name, version):
        if version == "init":
            init(module_name)
        elif version == "delete":
            delete(module_name)
        else:
            update(module_name, version)

    if module_name == "ALL":
        for name in ALL_NAMES:
            try:
                action(name, version)
            except ValueError as e:
                if 'neither' in e.args[0]:
                    continue
                raise
    else:
        action(module_name, version)
        if version not in ["init", "delete"]:
            run_test(module_name, version)
            build_package(module_name)
