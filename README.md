# PAX Express CLI
This is a CLI tool for using PAX.express.
It can be used to manage different things on the PAX.express service.
Please see the help after installation for further use cases.

Also check out the docs [here](https://github.com/paxexpress/docs)

## Installation

### Precompiled

From the [release page](https://github.com/paxexpress/paxexpress-cli/releases) binaries for Linux, MacOS and Windows can be downloaded.

They are single file executables.
No installer is provided as of this time.


### from source

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
