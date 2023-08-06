# -*- coding: utf-8 -*-
"""
    Sphinx test suite utilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2009 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import io
import shutil
import sys
import tempfile
from functools import wraps

from path import Path
from sphinx import application

__all__ = [
    "test_root",
    "raises",
    "raises_msg",
    "Struct",
    "ListOutput",
    "SphinxTestApplication",
    "with_app",
    "gen_with_app",
    "Path",
    "with_tempdir",
    "write_file",
    "sprint",
]


test_root = Path(__file__).parent.joinpath("root").abspath()


def _excstr(exc):
    if type(exc) is tuple:
        return str(tuple(map(_excstr, exc)))
    return exc.__name__


def raises(exc, func, *args, **kwds):
    """
    Raise :exc:`AssertionError` if ``func(*args, **kwds)`` does not
    raise *exc*.
    """
    try:
        func(*args, **kwds)
    except exc:
        pass
    else:
        raise AssertionError("%s did not raise %s" % (func.__name__, _excstr(exc)))


def raises_msg(exc, msg, func, *args, **kwds):
    """
    Raise :exc:`AssertionError` if ``func(*args, **kwds)`` does not
    raise *exc*, and check if the message contains *msg*.
    """
    try:
        func(*args, **kwds)
    except exc as err:
        assert msg in str(err), '"%s" not in "%s"' % (msg, err)
    else:
        raise AssertionError("%s did not raise %s" % (func.__name__, _excstr(exc)))


class Struct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class ListOutput(object):
    """
    File-like object that collects written text in a list.
    """

    def __init__(self, name):
        self.name = name
        self.content = []

    def reset(self):
        del self.content[:]

    def write(self, text):
        self.content.append(text)


class SphinxTestApplication(application.Sphinx):
    """
    A subclass of :class:`Sphinx` that runs on the test root, with some
    better default values for the initialization parameters.
    """

    def __init__(
        self,
        srcdir=None,
        confdir=None,
        outdir=None,
        doctreedir=None,
        buildername="html",
        confoverrides=None,
        status=None,
        warning=None,
        freshenv=None,
        warningiserror=None,
        tags=None,
        confname="conf.py",
        cleanenv=False,
    ):

        application.CONFIG_FILENAME = confname

        self.cleanup_trees = [test_root / "generated"]

        if srcdir is None:
            srcdir = test_root
        if srcdir == "(temp)":
            tempdir = Path(tempfile.mkdtemp())
            self.cleanup_trees.append(tempdir)
            temproot = tempdir / "root"
            test_root.copytree(temproot)
            srcdir = temproot
        else:
            srcdir = Path(srcdir)
        self.builddir = srcdir.joinpath("_build")
        if confdir is None:
            confdir = srcdir
        if outdir is None:
            outdir = srcdir.joinpath(self.builddir, buildername)
            if not outdir.isdir():
                outdir.makedirs()
            self.cleanup_trees.insert(0, outdir)
        if doctreedir is None:
            doctreedir = srcdir.joinpath(srcdir, self.builddir, "doctrees")
            if cleanenv:
                self.cleanup_trees.insert(0, doctreedir)
        if confoverrides is None:
            confoverrides = {}
        if status is None:
            status = io.StringIO()
        if warning is None:
            warning = ListOutput("stderr")
        if freshenv is None:
            freshenv = False
        if warningiserror is None:
            warningiserror = False

        application.Sphinx.__init__(
            self,
            srcdir,
            confdir,
            outdir,
            doctreedir,
            buildername,
            confoverrides,
            status,
            warning,
            freshenv,
            warningiserror,
            tags,
        )

    def cleanup(self, doctrees=False):
        for tree in self.cleanup_trees:
            shutil.rmtree(tree, True)


def with_app(*args, **kwargs):
    """
    Make a TestApp with args and kwargs, pass it to the test and clean up
    properly.
    """

    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            app = SphinxTestApplication(*args, **kwargs)
            func(app, *args2, **kwargs2)
            # don't execute cleanup if test failed
            app.cleanup()

        return deco

    return generator


def gen_with_app(*args, **kwargs):
    """
    Make a TestApp with args and kwargs, pass it to the test and clean up
    properly.
    """

    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            app = SphinxTestApplication(*args, **kwargs)
            for item in func(app, *args2, **kwargs2):
                yield item
            # don't execute cleanup if test failed
            app.cleanup()

        return deco

    return generator


def with_tempdir(func):
    def new_func():
        tempdir = Path(tempfile.mkdtemp())
        func(tempdir)
        tempdir.rmtree()

    new_func.__name__ = func.__name__
    return new_func


def write_file(name, contents):
    f = open(str(name), "wb")
    f.write(contents)
    f.close()


def sprint(*args):
    sys.stderr.write(" ".join(map(str, args)) + "\n")
