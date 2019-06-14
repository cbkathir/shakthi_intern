# verification-framework
This repository maintains the verification framework using python based [cocotb](https://github.com/potentialventures/cocotb)

## Contents
* [Setup](#setup)
  - [Dependencies](#deps)
* [Directory Structure](#dir-struct)
* [ECC](#ecc)

## Setup <a name="setup"></a>
## Dependencies <a name="deps"></a>
The following versions were used during the development and simulation
* Scripts: python 3.6
```sh
sudo apt-get install python3.6
sudo apt-get install python3.6-dev
```

## Clone repo
```sh
git clone --recursive https://gitlab.com/shaktiproject/verification_environment/py-uvm.git
```

## Directory Structure <a name="dir-struct"></a>
```
py-uvm
    ├── cocotb                  # Fixes env variables for verificaton
```
## Sample ECC test runs <a name="ecc"></a>
Be in the ``py-uvm`` directory 
```
$ export COCOTB=$PWD/cocotb
$ cd ecc/tests
$ make SIM=vcs
```
Verilator simulation (still in progress)
```
$ cp ecc/tests/Makefile.verilator cocotb/cocotb/share/makefiles/simulators/
$ cd ecc/tests
$ make SIM=verilator
```
