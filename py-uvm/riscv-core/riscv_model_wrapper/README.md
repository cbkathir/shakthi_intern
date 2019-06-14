# Spike Build
```sh
$ cd spike
$ mkdir build
$ export RISCV=$PWD/build
$ source build-spike-only.sh
```
# Spike Wrapper Build
```sh
$ cd <repo>/riscv-core/riscv_model_wrapper/spike_wrapper
$ cmake .
$ make
```
The `libslsvSpikeIf.so` is generated in the same directory

# Spike Wrapper memory map

Spike wrapper code generates the shared library file for spike with the following APIs 

| API      |      Are      |
|----------|-------------|
| CSpikeIf SpawnSpikeIF(char\* String) |  Create model instance and load elf  | 
| unsigned int CsingleStep(CSpikeIf instance) |    Do single step   |
| unsigned long long int CgetVariable(CSpikeIf instance,unsigned int SLSVaddress) | Get variable from model | 
| void DestroySpikeIF(CSpikeIf instance) | Delete model instance |

The address to be specified is defined by SLSV as a state id. A brief snapshot of the same is below:
| State ID |  Offset  | 
|----------|-------------|
| PC       |  `'h1020`  | 
| XPR      |  `'h1000`  | 
| FPR      | `'h1021`   |
| PRV      | `'h1041`   |
| SSTATUS  |   `'h100`  |
| SIE      |   `'h104`  |
| STVEC    |   `'h105`  |
| MSTATUS  |   `'h300`  |
| MISA     |   `'h301`  |
| MIE      |   `'h304`  |
| MTVEC    |   `'h305`  |

The CSR registers follow the offset address specified in the spike model (`encoding.h`)



