# GCC Compiler for Majumder's RISC-V Implementation

This collection of python scripts, as well as assembly and c header files lets you write a c program that compiles and assembles into binary data to be used on the MiniRisc-V Implementation.

<hr>

## Installation

In order for this compiler to work, you must have the riscv tool chain installed, specifically the one provided in UC-Berkeley's rocket-tools github repository. The repository can be found [here](https://github.com/freechipsproject/rocket-tools).
Installing the whole repository is not a bad idea, because it also comes with the spike simulator, which you can use to test your code before putting it on the RISC-V Core.

#### Installing the toolchain is as follows
``` bash
$ git clone https://github.com/freechipsproject/rocket-tools
$ git submodule update --init --recursive
$ export RISCV=path/to/where/you/want/toolchain/installed
```
Next you must edit the first two `build_project` lines in `build-rv32ima.sh` to build for rv32i by replacing `rv32ima` with `rv32i` for the `with-isa` and `with-arch` parameters.
'<br>
Then just run that script.
```bash
$ ./build-rv32ima.sh  
```
After the toolchain is installed, you'll need to make sure that it's in your PATH environment variable. Append the following line to your `~/.bashrc`:
```bash
export PATH="path/to/toolchain/bin:$PATH"
```

## Usage
```
usage: Mini-Risc-V-gcc.py [-h] [-c] files [files ...]

positional arguments:
  files       File Names (Takes .c and .s

optional arguments:
  -h, --help  show this help message and exit
  -c, --coe   generate .coe file instead of .hex file
```
