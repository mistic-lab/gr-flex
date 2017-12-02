
# GNU Radio Flex Blocks (gr-flex)

An out-of-tree GNU Radio block for communicating with the FlexRadio

### Architecture

![Architecture Diagram](https://cdn.rawgit.com/cjam/gr-flex/master/images/architecture.svg)

### References

[GNU Radio OOT Blocks](https://wiki.gnuradio.org/index.php/OutOfTreeModules)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

This project uses a .NET library called FlexlibMono which I have forked and included as a submodule within this project.  You will need to run

`git submodule update --init`

### Prerequisites

You will need the following pre-requisites installed on your machine (in this order):
> For OS-specific install instructions see the below sections for [Linux](#Linux) and [macOS](macOS).

- [GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR)
- [Python](https://www.python.org/) (**required by GNU Radio**, gr-flex was tested with 2.7)
- [Mono](http://www.mono-project.com/download/) **(only for MacOS/Linux systems)**
- [pip](https://pip.pypa.io/en/stable/installing/) **(already installed if Python 2 >=2.7.9 is installed)**
- [PythonNet]
- [cmake](cmake.org)


## Linux
> tested with Ubuntu 16.04

- GNU Radio
  ```
  sudo apt-get install gnuradio
  ```
- Mono
  ```
  sudo apt-get install mono-complete
  ```
- PythonNet **(if the following doesn't work, see the [troubleshooting](#troubleshooting) section)**
  ```
  sudo -H pip install pythonnet
  ```
- cmake
  ```
  sudo apt-get install cmake
  ```

## macOS
> tested with macOS 10.13 with [Homebrew](https://www.brew.sh/)

### Package manager
I've classically used MacPorts for everything but for this I went with Homebrew. Installing GNU Radio with Macports is supported and easy, but installing everything else is only well supported via brew. So take your pick. I opted for annoying gnuradio install and easy everything else install.

**Do not have both MacPorts and HomeBrew installed at once** - It'll just suck, probably. To uninstall MacPorts go to [their guide](https://guide.macports.org/chunked/installing.macports.uninstalling.html). They update it regularly so I don't want to copy out the commands here.


#### Install homebrew
Visit [their site](https://brew.sh/) where there will be up-to-date notes if you're on a weird or newer OS. The probably permanently useful install can be executed with:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Dependencies
- Xcode Command Line Tools
  ```
  xcode-select --installed
  ```
- [Python](https://www.python.org/download/releases/2.7/)

  It does require python 2.7 and although you probably definitely already have it installed on your system I went ahead and installed it again to make sure everything was up to date.

- [XQuartz/X11](https://www.xquartz.org/)

- GNU Radio

  This is the part that kind of sucks. You no longer have MacPorts installed so the recommended install of GNU Radio by the group that made GNU Radio doesn't apply. There is a brew package that will install GNU Radio, `brew install gnuradio` but since brew dropped support for qt4 in favour of qt5 the install leaves you without GNU Radio Companion which we want. You can bugger around with installing qt4 or you can check out [this handy repo](https://github.com/cfriedt/gnuradio-for-mac-without-macports) which allows you to install it as a `.app`.

- > pip (_Maybe not necessary. Try only setuptools below_)
  > ```
  > sudo easy_install pip
  > ```

- PKG-CONFIG
  ```
  brew install pkg-config
  ```

- glib 2
  ```
  brew install glib --universal
  ```

- Mono
  ```
  brew cask install mono-mdk
  ```
  ```
  PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Versions/{x.x.x}/lib/pkgconfig/
  ```

- setuptools
  ```
  brew install wget
  wget https://bootstrap.pypa.io/get-pip.py
  sudo -H python get-pip.py
  ```

- PythonNet **(if the following doesn't work, see the [troubleshooting](#troubleshooting) section)**
  ```
  git clone https://github.com/pythonnet/pythonnet
  cd pythonnet/
  ```
  ```
  python setup.py bdist_wheel
  ```
  > Look inside the newly created dist/ folder for the details of this command
  ```
  sudo pip install --user dist/pythonnet-{pythonnet version}-{cpython version}-{mac veresion}.whl
  ```

- cmake
  ```
  brew install cmake
  ```

- boost
  ```
  brew install boost
  ```

- doxygen
  ```
  brew install doxygen
  ```

### Installing the Block

Once all of the pre-requisites are installed, you can run the build script within the root of the project. A slight tweak needs to be made if GNU Radio was installed using PyBombs. For a non-pybombs install:
```
cd REPO_DIRECTORY
sudo ./build.sh
```

For a PyBombs install of GNU Radio, you need to open the script and comment out (prepend with a #) the following few lines near the bottom which say:
```
cmake ../
make
sudo make install
```

Then to install:
```
cd REPO_DIRECTORY
sudo ./build.sh
cd build/
cmake -DCMAKE_INSTALL_PREFIX=/FULL/PATH/TO/PYBOMBS/PREFIX ../
sudo make
sudo make install
```

This script will do some or all of the following (depending on which version of the install you used):

- Build the Flexlib Mono project with MSBuild (Release Configuration)
- Copy the resulting binaries into the gr-flex module
- create a `build/` directory
- runs `CMake`  (configures make files)
- runs `make`   (builds python module)
- runs `sudo make install`  (installs block into GNU Radio directory)

Here's some sample output from the script (installing into the GNU Radio folders):
![Build Output](./images/build-output.png)

### Using the Block
Here's how the **Flex Source** block currently looks in GNU Radio:

![Flex Block](./images/flex-source-block.png)

If you installed GNU Radio via PyBombs, then running the block may cause GNU Radio to throw weird library errors. Check out the [troubleshooting section](#library-errors) for more info.

### Sample Apps
See the sample **GRC** files that have been placed into the `examples/` directory of this repo:

`./examples/flex-source.grc` - sends FlexRadio data to a waterfall plot

## Running the Samples

Running the sample GRC files will show output from the gr-flex block that could potentially help with troubleshooting problems.

The FlexRadio has a discovery mechanism that works on the local area network to allow for applications to discover and configure themselves to interact with the FlexRadio.  

When the Flex Source starts up, it will go through the discovery process and output the results within the terminal.

![Sample Output](./images/sample-output.png)

## Troubleshooting

### PythonNet
If you're having problems installing [PythonNet](#pythonnet) the following may help. We have no idea why some of these things work, but if they're listed below it was part of our solution. There is [a documented problem](https://github.com/pythonnet/pythonnet/issues/555) at the time of this writing (Nov. 2017) to get PythonNet running with Mono.

- [setuptools](pypi.python.org/pypi/setuptools) **(At least on Ubuntu 16.04, setuptools is likely outdated which causes problems installing pip as well as pythonnet)**. To check which version you have, run:
```python
python
import setuptools
setuptools.__version__
```
The current version is listed at https://pypi.python.org/pypi/setuptools.
If you need to upgrade it:
```
wget https://bootstrap.pypa.io/get-pip.py
sudo -H python get-pip.py
```
If in Linux (Ubuntu), run:
```
sudo -H pip install setuptools --upgrade
```

- [gliblib](https://packages.ubuntu.com/xenial/libglib2.0-dev)
```
sudo apt-get install libglib2.0-dev
```

- Finally, try installing pythonnet using an egg by running:
```
sudo pip install git+https://github.com/pythonnet/pythonnet --egg
```

### Library errors
If you see the following error or similar from GNU Radio when trying to run a flowgraph, this section may help you.
```
Generating: '/home/username/Documents/gr-flex/examples/top_block.py'
>>> Warning: This flow graph may not have flow control: no audio or RF hardware blocks found. Add a Misc->Throttle block to your flow graph to avoid CPU congestion.

Executing: /usr/bin/python2 -u /home/username/Documents/gr-flex/examples/top_block.py

Traceback (most recent call last):
  File "/home/username/Documents/gr-flex/examples/top_block.py", line 19, in <module>
    from gnuradio import blocks
  File "/home/username/prefix/default/lib/python2.7/dist-packages/gnuradio/blocks/__init__.py", line 32, in <module>
    from blocks_swig import *
  File "/home/username/prefix/default/lib/python2.7/dist-packages/gnuradio/blocks/blocks_swig.py", line 22, in <module>
    from blocks_swig0 import *
  File "/home/username/prefix/default/lib/python2.7/dist-packages/gnuradio/blocks/blocks_swig0.py", line 28, in <module>
    _blocks_swig0 = swig_import_helper()
  File "/home/username/prefix/default/lib/python2.7/dist-packages/gnuradio/blocks/blocks_swig0.py", line 24, in swig_import_helper
    _mod = imp.load_module('_blocks_swig0', fp, pathname, description)
ImportError: libgnuradio-blocks-3.7.12git.so.0.0.0: cannot open shared object file: No such file or directory

>>> Done (return code 1)
```

Run locate, and make sure that the files do exist.
```
$ locate libgnuradio-blocks-3.7.12git.so.0.0.0
/home/username/prefix/default/lib/libgnuradio-blocks-3.7.12git.so.0.0.0
/home/username/prefix/default/src/gnuradio/build/gr-blocks/lib/libgnuradio-blocks-3.7.12git.so.0.0.0
```

In this case, the path to the library is `/home/username/prefix/default/lib` and apparently python isn't looking there. Run `ldconfig -p` to see whether it is looking in the prefix folder. If not, the following got me going.
```
sudo su
echo "/home/username/prefix/default/lib" > /etc/ld.so.conf.d/local.conf
ldconfig
```
Now exit `su` and check with `ldconfig -p` whether it's now looking in the prefix folder. If so, you should be good to go.

## Running the tests

Unfortunately since the block requires the presence of a FlexRadio, it makes mocking the block much harder to do.  To test this module, the sample apps were used with a Flex system to test and confirm functionality.

## Built With

* [CMAKE](https://cmake.org/) - CMake
* [MSBuild](http://www.mono-project.com/docs/tools+libraries/tools/xbuild/) - MSBuild (Mono)
* [PythonNet]
* [GNU Radio]

## Contributing

Pull Requests are welcome.

## Authors

* **Colter Mcquay** - *Initial work*
* **Nicholas Bruce** - *Follow up slave-labour*

See also the list of [contributors](https://github.com/cjam/gr-flex/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thanks to the following students who wrote some reports that provided some insight / approaches to solving this problem.

- Robert Cormier
- Marian Böhm
- Donatus Unuigboje

Thanks to [Frank Werner-Krippendorf](https://github.com/krippendorf) for the work on the [FlexlibMono](https://github.com/krippendorf/FlexlibMono) project which I forked and used as a submodule within this repository.

[GNU Radio]: https://wiki.gnuradio.org/index.php/InstallingGR "GNU Radio"
[PythonNet]: https://pythonnet.github.io/ "Python.Net"
[Mono]: http://www.mono-project.com/download/ "Mono"
