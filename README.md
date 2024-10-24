siteconf
========

Customizes `sys.path` based on platform and Python version when Python loads for site-specific configuration.

This `sitecustomize.py` module plays a crucial role in VFX pipelines by allowing customizations to be applied to the Python environment at startup.

https://docs.python.org/3/library/site.html#module-sitecustomize

Siteconf works best combined with [envstack](https://github.com/rsgalloway/envstack).

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

## Usage

The `sitecustomize.py` module provides a convenient way to customize the Python environment by executing code before the interpreter begins executing the main script.

Python libraries are resolved in the following order, from most specific to most agnostic:

    $ROOT/$ENV/lib/$PLATFORM/python[$PYVERSION]
    $ROOT/$ENV/lib/$PLATFORM/python
    $ROOT/$ENV/lib/python[$PYVERSION]
    $ROOT/$ENV/lib/python

Some defaults have been set for convenience that can be overridden with [environment variables](#environment-variables).

For example, by default the deployment root is called "tools", the production environment is called "prod" and the development environment is called "dev", so by default on linux `sys.path` would include:

```bash
/mnt/tools/prod/lib/linux/python3
/mnt/tools/prod/lib/linux/python
/mnt/tools/prod/lib/python3
/mnt/tools/prod/lib/python
```

or on Windows:

```shell
X:/tools/prod/lib/win32/python3
X:/tools/prod/lib/win32/python
X:/tools/prod/lib/python3
X:/tools/prod/lib/python
```

## Environment Variables

The following environment variables can be used to customize Python search paths:

| Variable         | Description |
|------------------|-------------|
| $DEFAULT_ENV_DIR | envstack default env directory |
| $DEV             | add development environment to the search path |
| $DEV_ENV         | override the default development environment name "dev" |
| $DRIVE_LETTER    | override the default Windows drive letter name "Z" |
| $ENV             | add a custom environment to the search path, e.g. "test" |
| $PLATFORM        | override the platform name (win32, linux, osx) |
| $PROD_ENV        | override the default production environment name "prod" |
| $PYVERSION       | Python version (e.g. 2, 3 or 3.11) |
| $ROOT            | Python module deployment path including mount point |
| $USE_UNC         | use UNC paths on Windows |


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
$ ENV=test DEPLOY_ROOT=path/to/tools PYVERSION=3.11 python sitecustomize.py 
/mnt/path/to/tools/test/lib/linux/python3.11
/mnt/path/to/tools/test/lib/linux/python
/mnt/path/to/tools/test/lib/python3.11
/mnt/path/to/tools/test/lib/python
/mnt/path/to/tools/prod/lib/linux/python3.11
/mnt/path/to/tools/prod/lib/linux/python
/mnt/path/to/tools/prod/lib/python3.11
/mnt/path/to/tools/prod/lib/python
```

## Deployment

A few notes about deployment of Python modules and packages:

- platform agnostic libs should be deployed to `lib`
- platform specific libs should be deployed to `lib/$PLATFORM`
- Python version agnostic libs should be deployed to `python`
- Python version specific libs should be deployed to `python2`, `python3`, `python3.11`, etc.
