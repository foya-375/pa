# ProgressApplyer
A tool that allows you to execute a set of commands that should run in another directory without switching directories.
It is written using Python and Bash script, extremely simple but incredibly useful.

## Platform
Unix-like OSes that use Bash are supported, but Windows platforms are not.

## Installation & Usage
__python3 interpreter is required before you install this program.__

1. Clone this repo to anywhere you like.
2. Use `pip install -r requirements.txt` to install additional requirements. __Note that the packages must be installed system-wide.__
3. Configure the program inside ~/.pa_conf.yaml, here is an example of it:
``` yaml
ns_init:
  path: ~/ns-3.29/
  commands:
    - ./waf clean
    - ./waf configure --enable-examples --enable-tests --disable-werror
    - ./waf build

ns_build:
  path: ~/ns-3.29/
  commands:
    - ./waf build
```
4. Launch this program using: `./pa -n progress-name [-e] [-d]` like this: `./pa -n ns_init`

You can put this inside your bashrc which could saves your time of typing:
``` bash
function pa() {
  source /path/to/pa $@
}
```
Then you can just type `pa -n [progress name]` anywhere.
