from update import run_test, build_package, ALL_NAMES
import sys

_, name, version = sys.argv

if name == "ALL":
    names = ALL_NAMES
else:
    names = [name]

for name in ALL_NAMES:
    if name == "chunk":
        continue
    run_test(name, version)
    build_package(name)
