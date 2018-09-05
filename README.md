It is assumed that source files are stored in "./sources" and testbench files are stored in "./testbench"

to run all version of Vivado HLS in your environment (/opt/Xilinx/Vivado)

```
TARGET=exmaple ./auto_vivado_hls.sh 
```

The output result is in analysis_result.csv, if you have Python.

to specify Vivado installed directory

```
VIVADO=/home/Vivado TARGET=exmaple ./auto_vivado_hls.sh 
```

to specify version for IP-core

```
VERSION=2.1 TARGET=example ./auto_vivado_hls.sh 
```

to specify target period list

```
TARGET_PERIOD=10:20 VERSION=2.1 TARGET=example ./auto_vivado_hls.sh 
```
