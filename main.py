import glob
import importlib
from os.path import *


def main():
    module = run_latest()
    module.main()


def find_versions():
    modules = glob.glob(join(dirname(__file__), "version", "*.py"))
    __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
    return __all__


def determine_latest():
    versions = find_versions()
    latest = "unNote_v000"
    for f in versions:
        if f[0:8] == "unNote_v":
            if int(f[8:11]) > int(latest[8:11]):
                latest = f
    return latest


def run_latest():
    file = determine_latest()
    file = "." + file
    module = importlib.import_module(file, package="version")
    return module


if __name__ == '__main__':
    main()
