** NOTE ** This project is no longer actively developed!

# Can I Use Python 3?

[![Build Status](https://travis-ci.org/brettcannon/caniusepython3.svg?branch=master)](https://travis-ci.org/brettcannon/caniusepython3)

You can read the documentation on how to use caniusepython3 from its
[PyPI page](https://pypi.python.org/pypi/caniusepython3). A [web interface](https://github.com/jezdez/caniusepython3.com)
is also available.

# How do you tell if a project has been ported to Python 3?

On [PyPI](https://pypi.python.org/) each project can specify various
[trove classifiers](https://pypi.python.org/pypi?%3Aaction=list_classifiers)
(typically in a project's `setup.py` through a [`classifier`](https://docs.python.org/3/distutils/setupscript.html#additional-meta-data)
argument to `setup()`).
There are various classifiers related to what version of Python a project can
run on. E.g.:

    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.0
    Programming Language :: Python :: 3.1
    Programming Language :: Python :: 3.2
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7

As long as a trove classifier for some version of Python 3 is specified then the
project is considered to support Python 3 (project owners: it is preferred you
**at least** specify `Programming Language :: Python :: 3` as that is how you
end up listed on the [Python 3 Packages list on PyPI](https://pypi.python.org/pypi?%3Aaction=packages_rss);
you can represent Python 2 support with `Programming Language :: Python`). Note
that Python 3.0 through 3.4 have reached their [End Of Life](https://docs.python.org/devguide/index.html#branchstatus).

The other way is through a [manual override](https://github.com/brettcannon/caniusepython3/blob/master/caniusepython3/overrides.json) in
`caniusepython3` itself. Projects ends up on this list because:

- They are now part of [Python's standard library](http://docs.python.org/3/py-modindex.html) in some release of Python 3
- Their Python 3 port is under a different name
- They are missing a Python 3 trove classifier but have actually been ported

If any of these various requirements are met, then a project is considered to
support Python 3 and thus will be added to the manual overrides list. You can
see the list of overrides when you use caniusepython3's CLI with verbose output
turned on.

## What if I know of a project that should be added to the overrides file?

If a project has Python 3 support in a release on PyPI but they have not added the
proper trove classifier, then either submit a
[pull request](https://github.com/brettcannon/caniusepython3/pulls) or file an
[issue](https://github.com/brettcannon/caniusepython3/issues) with the name of the
project and a link to some proof that a release available on PyPI has indeed been
ported (e.g. PyPI page stating the support, tox.ini file showing tests being run
against Python 3, etc.). Projects that have Python 3 support in their version control
system but not yet available on PyPI will **not** be considered for inclusion in the
overrides file.

# How can I get a project ported to Python 3?

Typically projects which have not switched to Python 3 yet are waiting for:

- A dependency to be ported to Python 3
- Someone to volunteer to put in the time and effort to do the port

Since `caniusepython3` will tell you what dependencies are blocking a project
that you depend on from being ported, you can try to port a project farther
down your dependency graph to help a more direct dependency make the transition.

Which brings up the second point: volunteering to do a port. Most projects
happily accept help, they just have not done the port yet because they have
not had the time ("volunteering" can also take the form of paying someone to do
the port on your behalf). Some projects are simply waiting for people to ask for it,
so even speaking up politely and requesting a port can get the process started.

If you are looking for help to port a project, you can always search online for
various sources of help. If you want a specific starting point there are
[HOWTOs](http://docs.python.org/3/howto/index.html) in the Python documentation
on [porting pure Python modules](http://docs.python.org/3/howto/pyporting.html)
and [extension modules](http://docs.python.org/3/howto/cporting.html).

# Can I use it as a pre-commit hook?

Yes! Begin by installing [pre-commit](https://pre-commit.com/):

```
pip install pre-commit
pre-commit install
```

You can add the following hook in your `.pre-commit-config.yaml` file.

```yaml
    - repo: https://github.com/brettcannon/caniusepython3
      rev: v7.1.0  # Update as desired to new releases/tags
      hooks:
          - id: caniusepython3
            files: requirements\.txt$  # Update to match your requirements files accordingly.
            args: [
                -r  # Causes caniusepython3 to treat the `files` argument as a requirements file.
          ]
            stages: [commit]  # Change it to `manual`, if `caniusepython3` takes too long between commits, so as to only run them manually in build jobs.
```

If you are running manually somewhere, we can run the following command:

```
pre-commit run --hook-stage manual caniusepython3 --files  requirements.txt
```

# Change Log

# 7.3.0

- Usual overrides updates
- Removed argparse as a requirement
- Added Python 3.9 support
- Silenced a warning from setuptools about importing distutils (via distlib)
  before setuptools itself
- Made it a bit more clear that false-negatives are possible (by design)
- Marked the project as retired

# 7.2.0

- Add an `--index`/`-i` flag to specify an index URL (thanks [macleodbroad-wf](https://github.com/macleodbroad-wf))
- Add support for [pre-commit](https://pre-commit.com/) (thanks [Milind Shakya](https://github.com/milind-shakya-sp))
- Update overrides data (thanks [Andriy Yablonskyy](https://github.com/yablonsky))

# 7.1.0

- Remove unused imports from Pylint checker
- Usual overrides updates
- Introduce the `--exclude` flag (thanks [Milind Shakya](https://github.com/milind-shakya-sp))

# 7.0.0

- Drop Python 3.3 support
- Usual overrides updates

# 6.0.0

- Refactor some code to avoid a warning in Python 3.6
- Stop calling pip's internals (pip 10 would break everything)
- Fix "No handler found" output under Python 2.7
  (patch by [arnuschky](https://github.com/arnuschky))
- Usual overrides updates

# 5.0.0

- Return a `3` error code when a command completes successfully but there are
  found blockers (patch by [pcattori](https://github.com/pcattori);
  accidentally left out of the 4.0.0 release)
- Officially support Python 3.6
- Usual overrides updates

# 4.0.0

- Stop using PyPI's XML-RPC API and move to its JSON one for better performance
  (and switch to https://pypi.org)
- Load the overrides data from GitHub when possible, falling back to the data
  included with the package when necessary (thanks to
  [shafrom](https://github.com/shaform) for adding local, one-day caching)

# 3.4.1

- Update the URL used for PyPI to https://pypi.org
  (patch by [Chris Fournier](https://github.com/cfournie))
- Usual override updates

# 3.4.0

- Fix a dict comprehension failure with the pylint checker
  (patch by [Jeroen Oldenburger](https://github.com/jeroenoldenburger))
- Usual override updates
- Python 3.5 support
- Tests have been made less flaky
- Use pypi.io instead of pypi.python.org
- Normalize project names to help guarantee lookup success

# 3.3.0

- Made tests more robust in the face of PyPI timing out
- Added Python 3.5 support
- Dropped Python 2.6 and 3.2 support
- Updated tests to not use Twisted as a Python 2-only project
- Fixed a bug where the pylint checker was incorrectly missing `from __future__ import unicode_literals` ([issue #103](https://github.com/brettcannon/caniusepython3/issues/103); reported by [David Euresti](https://github.com/euresti))
- Usual overrides updates

# 3.2.0

- Fix a failing test due to the assumed unported project being ported =)
- Work around distlib 0.2.0 bug (patch by @rawrgulmuffins)
- Usual override updates

# 3.1.0

- Log more details when running under `-v` (patch by @msabramo)
- Print a 🎉 -- it's a party popper in case you have mojibake for it -- when the
  terminal supports it and there are no blocking dependencies (patch by @msabramo)
- Fix compatibility with pip 6.1.0 (patch by @msabramo)
- Fix warning of missing logger when using `setup.py` integration
  (issue #80; patch by @msabramo)
- Remove checkers for `filter`, `map`, `range`, and `zip` as they have been
  improved upon and
  [merged upstream in Pylint](https://bitbucket.org/logilab/pylint/pull-request/216/warn-when-filter-map-range-and-filter-are/diff)
- Updated outdated documentation
- Usual override updates

# 3.0.0

- Introduce `caniusepython3.pylint_checker` which extends `pylint --py3k` with
  very strict porting checks
- Work around a [bug in distlib](https://bitbucket.org/pypa/distlib/issue/58/distliblocatorslocate-returning-an-empty)
- Compatibility fix for pip 6.0 ([issue #72](https://github.com/brettcannon/caniusepython3/issues/72))
- Usual override updates

# 2.2.0

- Suppress an `xmlrpclib.Fault` exception under Python 2.6 when trying to close
  an XML-RPC connection (can't close a connection under Python 2.6 anyway and
  the exception has only been seen on [Travis](https://travis-ci.org/))
- Move to [unittest2](https://pypi.python.org/pypi/unittest2) as a developer
  dependency
- Move [mock](https://pypi.python.org/pypi/mock) to a developer dependency
- Usual override tweaks

# 2.1.2

- Avoid infinite recursion when there is a circular dependency
  ([issue #60](https://github.com/brettcannon/caniusepython3/issues/60))
- Usual overrides tweaks

# 2.1.1

- Normalize the names of direct dependencies for proper Python 3 compatibility
  checking
  ([issue #55](https://github.com/brettcannon/caniusepython3/issues/55))
- Properly set the logging details when executed from the entry point
- Usual overrides tweaks

## 2.1.0

- Verbose output will print what manual overrides are used and why
  (when available)
- Fix logging to only be configured when running as a script as well as fix a
  format bug
- Usual override updates

## 2.0.3

- Fixed `setup.py caniusepython3` to work with `extras_require` properly
- Fix various errors triggered from the moving of the `just_name()` function to
  a new module in 2.0.0 (patch by Vaibhav Sagar w/ input from Jannis Leidel)
- Usual overrides tweaks (thanks to CyrilRoelandteNovance for contributing)

## 2.0.2

- Fix lack of unicode usage in a test
- Make Python 2.6 happy again due to its distate of empty XML-RPC results

## 2.0.1

- Fix syntax error

## 2.0.0

- Tweak overrides
- `-r`, `-m`, and `-p` now take 1+ arguments instead of a single comma-separated
  list
- Unrecognized projects are considered ported to prevent the lack of info on
  the unrecognized project perpetually suggesting that it's never been ported
- Introduced `icanusepython3.check()`

## 1.2.1

- Fix `-v` to actually do something again
- Tweaked overrides

## 1.2.0

- `-r` accepts a comma-separated list of file paths

## 1.1.0

- Setuptools command support
- Various fixes

## 1.0

Initial release.
