sitecustomize
=============

Customizes `sys.path` based on platform and Python version when Python loads
for site-specific configuration.

https://docs.python.org/3/library/site.html#module-sitecustomize

This `sitecustomize.py` module plays a crucial role in VFX pipelines by allowing customizations to be applied to the Python environment at startup.

## Installation

To install the `sitecustomize` module, follow these steps:

```bash
$ git clone https://github.com/rsgalloway/sitecustomize
$ cd sitecustomize
$ python setup.py install
```

## Usage

`sitecustomize.py` provides a convenient way to customize the Python environment by executing code before the interpreter begins executing the main script.

Python libraries are resolved in the following order, from most specific to most agnostic:

    $ROOT/$ENV/lib/$OS/python[$PYVERSION]
    $ROOT/$ENV/lib/$OS/python
    $ROOT/$ENV/lib/python[$PYVERSION]
    $ROOT/$ENV/lib/python

Some defaults have been set for convenience that can be overridden with [environment variables](#environment-variables).

For example, by default the deployment root is called "tool", the production environment is called "prod" and the development environment is called "dev", so by default on linux `sys.path` would include:

```bash
/mnt/tool/prod/lib/linux/python3
/mnt/tool/prod/lib/linux/python
/mnt/tool/prod/lib/python3
/mnt/tool/prod/lib/python
```

or on Windows:

```shell
Z:/tool/prod/lib/win64/python3
Z:/tool/prod/lib/win64/python
Z:/tool/prod/lib/python3
Z:/tool/prod/lib/python
```

## Environment Variables

The following environment variables can be used to customize Python search paths:

| Variable      | Description |
|---------------|-------------|
| $DEPLOY_ROOT  | override the default deployment path "tool" |
| $DEV          | add development environment to the search path |
| $DEV_ENV      | override the default development environment name "dev" |
| $DRIVE_LETTER | override the default Windows drive letter name "Z" |
| $ENV          | add a custom environment to the search path, e.g. "test" |
| $OS           | override the platform name (win64, linux, osx) |
| $PROD_ENV     | override the default production environment name "prod" |
| $PYVERSION    | Python version (e.g. 2, 3 or 3.11) |
| $ROOT         | Python module deployment path including mount point |
| $USE_UNC      | use UNC paths on Windows |


## Development Environment

To add development versions of Python libs (supercedes prod):

```bash
$ export DEV=1
```

Now, the dev environment takes precedence over prod, but the prod environment is still in sys.path, just lower down in priority, so anything in dev will override anything else:

```bash
/mnt/tool/dev/lib/linux/python3
/mnt/tool/dev/lib/linux/python
/mnt/tool/dev/lib/python3
/mnt/tool/dev/lib/python
/mnt/tool/prod/lib/linux/python3
/mnt/tool/prod/lib/linux/python
/mnt/tool/prod/lib/python3
/mnt/tool/prod/lib/python
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
- platform specific libs should be deployed to `lib/$OS`
- Python version agnostic libs should be deployed to `python`
- Python version specific libs should be deployed to `python2`, `python3`, `python3.11`, etc.

## Contributing

If you have suggestions, bug reports, or would like to contribute to the `sitecustomize` module, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/rsgalloway/sitecustomize).