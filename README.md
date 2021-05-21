# PAX Express CLI
This is a CLI tool for using PAX.express.
It can be used to manage different things on the PAX.express service.
Please see the help after installation for further use cases.

Also check out the docs [here](https://github.com/paxexpress/docs)

## Installation

### pipx

If you know and have `pipx` it is the preferred way of installing the paxexpress CLI is via [pipx](https://github.com/pipxproject/pipx):

```
pipx install paxexpress-cli
```


### Compiled

The PAX.express CLI is built with python.
If you have python installed, it is recommended to use pipx to install it.
If you do not have python we provide an executable that bundles python and all dependencies into a single file.
These are slower than using pax.express directly via your system python.

MacOS and Windows binaries are can be downloaded from the [release page](https://github.com/paxexpress/paxexpress-cli/releases).


### From source

Clone this repository from GitHhub.

If you just which to use the current git version, without doing any development work on it:

```shell
poetry install --no-dev
```

To also install development tools:

```shell
poetry install
```

To run the cli use:

```
poetry run paxexpress --help
```
