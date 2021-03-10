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

Will result in a single file named `paxexpress.bin`

### Windows
```shell
poetry install
poetry shell
for %i in (where paxexpress) do @python.exe -m nuitka --standalone --include-module typing_extensions  --include-package email_validator  --onefile --include-package win32ctypes  --follow-imports --windows-onefile-tempdir --windows-company-name=`company name` --windows-product-version=`version name` %~$PATH:i
```
Will result in a single file named `paxexpress.exe`



### Mac OS X
```shell
poetry install
poetry shell
python -m nuitka --follow-imports $(which paxexpress)
```
Will result in a single file named `paxexpress.bin`
