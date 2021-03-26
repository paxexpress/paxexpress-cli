# Releasing

## Tag

 * git tag `vX.Y.Z`


## Building binaries

We use [PyOxidizer](https://github.com/indygreg/PyOxidizer) and [warp](https://github.com/dgiagio/warp) to build binaries for different platforms.

### Linux

```shell
pyoxidizer build --release

cd build/x86_64-[distribution]-linux-gnu/release

curl -Lo warp-packer https://github.com/dgiagio/warp/releases/download/v0.3.0/linux-x64.warp-packer

chmod +x warp-packer

./warp-packer -a macos-x64 -i install -e paxexpress -o paxexpress

./warp-packer --arch linux-x64 --input_dir install --exec paxexpress --output paxexpress

chmod +x paxexpress

```

Will result in a single file named `paxexpress`

### Windows

download the warp from [windows warp packer](https://github.com/dgiagio/warp/releases/download/v0.3.0/windows-x64.warp-packer.exe)

```shell
pyoxidizer build --release

cd \build\x86_64-pc-windows-msvc\release

.\warp-packer --arch windows-x64 --input_dir .\install\ --exec paxexpress.exe --output paxexpress.exe

```

Will result in a single file named `paxexpress.exe`

### Mac OS X

```shell
pyoxidizer build --release

cd  ./build/x86_64-apple-darwin/release

curl -Lo warp-packer https://github.com/dgiagio/warp/releases/download/v0.3.0/macos-x64.warp-packer

chmod +x warp-packer

./warp-packer -a macos-x64 -i install -e paxexpress -o paxexpress

```

Will result in a single file named `paxexpress`
