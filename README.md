siteconf
========

Customizes `sys.path` based on platform and Python version when Python loads for site-specific configuration.

This `sitecustomize.py` module plays a crucial role in VFX pipelines by allowing customizations to be applied to the Python environment at startup.

https://docs.python.org/3/library/site.html#module-sitecustomize

## Installation

The easiest way to install is with pip:

```bash
$ pip install siteconf
```

Alternatively, to install from the repo follow these steps:

```bash
$ git clone https://github.com/rsgalloway/siteconf
$ cd siteconf
$ python setup.py install
```


#### distman

Alternate installation using [distman](https://github.com/rsgalloway/distman):

```bash
$ distman [-d]
```

## Usage

The `sitecustomize.py` module provides a convenient way to customize the Python environment by executing code before the interpreter begins executing the main script.

Python libraries are resolved in the following order, from most specific to most agnostic:

    $ROOT/$ENV/lib/$PLATFORM/python[$PYVERSION]
    $ROOT/$ENV/lib/$PLATFORM/python
    $ROOT/$ENV/lib/python[$PYVERSION]
    $ROOT/$ENV/lib/python

Some defaults have been set for convenience that can be overridden with [environment variables](#environment-variables).

For example, if `$ROOT` is `/mnt/tools` and the production environment is `prod`,
then by default on linux `sys.path` would include:

```bash
/mnt/tools/prod/lib/linux/python3
/mnt/tools/prod/lib/linux/python
/mnt/tools/prod/lib/python3
/mnt/tools/prod/lib/python
```

or on Windows if `$ROOT` is `X:/tools`:

```shell
X:/tools/prod/lib/win32/python3
X:/tools/prod/lib/win32/python
X:/tools/prod/lib/python3
X:/tools/prod/lib/python
```

### whichpy

whichpy is the Python equivalent of which: it's a simple command line utility
that tells you the location of Python modules and packages:

```bash
$ whichpy envstack
/path/to/the/envstack/package
```

This can be useful when Python modules and packages are contextual and can live
in different places depending on your cwd.

## Environment Variables

The following environment variables can be used to customize Python search paths:

| Variable         | Description |
|------------------|-------------|
| $DEFAULT_ENV_DIR | envstack default .env file directory |
| $DEV             | add development environment to the search path |
| $DEV_ENV         | override the default development environment name "dev" |
| $ENV             | add a custom environment to the search path, e.g. "test" |
| $PLATFORM        | override the platform name (win32, linux, osx) |
| $PROD_ENV        | override the default production environment name "prod" |
| $PYVERSION       | Python version (e.g. 2, 3 or 3.11) |
| $ROOT            | Python module deployment path including mount point |


## Development Environment

To add development versions of Python libs (supercedes prod):

```bash
$ export DEV=1
```

Now, the dev environment takes precedence over prod, but the prod environment is still in sys.path, just lower down in priority, so anything in dev will override anything else:

```bash
/mnt/tools/dev/lib/linux/python3
/mnt/tools/dev/lib/linux/python
/mnt/tools/dev/lib/python3
/mnt/tools/dev/lib/python
/mnt/tools/prod/lib/linux/python3
/mnt/tools/prod/lib/linux/python
/mnt/tools/prod/lib/python3
/mnt/tools/prod/lib/python
```

To add a custom "test" environment to the Python search path (supercedes all others):

    $ export ENV="test"

Custom environments can be useful for testing a developer's test environment.

To get an idea how environment variables can be set to customize the Python search path here is an example that includes a custom env "test" and Python version 3.11 on linux:

```bash
$ ENV=test ROOT=/mnt/deploy PYVERSION=3.12 python -m sitecustomize.py 
/mnt/deploy/test/lib/linux/python3.12
/mnt/deploy/test/lib/linux/python
/mnt/deploy/test/lib/python3.12
/mnt/deploy/test/lib/python
/mnt/deploy/prod/lib/linux/python3.12
/mnt/deploy/prod/lib/linux/python
/mnt/deploy/prod/lib/python3.12
/mnt/deploy/prod/lib/python
```

## Deployment

A few notes about deployment of Python modules and packages:

- platform agnostic libs should be deployed to `lib`
- platform specific libs should be deployed to `lib/$PLATFORM`
- Python version agnostic libs should be deployed to `python`
- Python version specific libs should be deployed to `python2`, `python3`, `python3.11`, etc.
