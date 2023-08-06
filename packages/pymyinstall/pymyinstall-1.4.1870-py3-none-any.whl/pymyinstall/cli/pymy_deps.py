#!python
"""
script which looks into the dependencies for a module

.. todoext::
    :title: add a script to look into dependencies
    :tag: done
    :cost: 0.5
    :date: 2016-09-18
    :hidden:
    :release: 1.1

    Add a script to check the missing dependencies.

.. versionadded:: 1.1
"""
from __future__ import print_function
import sys
import os
import argparse


def get_parser():
    """
    defines the way to parse the script ``pymy_deps``
    """
    parser = argparse.ArgumentParser(
        description='look dependencies for modules')
    parser.add_argument(
        'module',
        nargs="*",
        default="all",
        help='update only the list of modules included in this list or all modules if not specified or equal to all')
    return parser


def do_main(list_modules=None):
    """
    calls function @see fn missing_dependencies

    @param      list_modules     list of modules to update or None for all
    """
    try:
        from pymyinstall.installhelper import missing_dependencies, get_module_dependencies
    except ImportError:
        pfolder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(pfolder)
        if "pymyinstall" in sys.modules:
            del sys.modules["pymyinstall"]
        if "pymyinstall.installhelper" in sys.modules:
            del sys.modules["pymyinstall.installhelper"]
        try:
            from pymyinstall.installhelper import missing_dependencies, get_module_dependencies
        except ImportError as e:
            mes = "pfolder={0}\nPATH:\n{1}".format(
                pfolder, "\n".join(sys.path))
            raise ImportError(mes) from e
    res = missing_dependencies(list_modules)
    if len(res) > 0:
        for r in res:
            print(r)
    elif list_modules is not None and len(list_modules) > 0:
        for mod in list_modules:
            print("checking ", mod)
            res = get_module_dependencies(mod)
            for r, v in sorted(res.items()):
                print("  ", r, v)
    else:
        print("no missing dependencies")


def main():
    """
    calls function @see fn missing_dependencies but is meant to be added to scripts folder,
    parse command line arguments
    """
    parser = get_parser()
    try:
        res = parser.parse_args()
    except SystemExit:
        print(parser.format_usage())
        res = None

    if res is not None:
        list_module = None if res.module in [
            "all", "", "-", None, []] else res.module
        do_main(list_modules=list_module)


if __name__ == "__main__":
    main()
