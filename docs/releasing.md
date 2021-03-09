# Releasing

## Tag

 * git tag `vX.Y.Z`


## Building binaries

We use [nuitka](https://nuitka.net/) to build binaries for different platforms.

### Linux

```shell
poetry install
poetry shell
python -m nuitka --standalone --no-prefer-source-code --linux-onefile-icon 'pax_express_client/icon.png' --include-module typing_extensions --include-package email_validator --onefile --follow-imports $(which paxexpress)
```

Will result in a single file named `paxcounter.bin`

### Windows


### Mac OS X