#!/bin/sh

if [ -z "$VIVADO" ]; then
	VIVADO=/opt/Xilinx/Vivado
fi
if [ -z "$VERSION" ]; then
	VERSION=1.0
fi
if [ -z "$TARGET_PERIOD" ]; then
	TARGET_PERIOD="10:5:4:3.33:2.5:2:1.56"
fi
if [ -z "$TARGET" ]; then
	echo "set TAREGET environment"
	exit 1
fi

echo "used Vivado tools in" ${VIVADO}
echo "target function" ${TARGET}
echo "output IP-core version" ${VERSION}

function run_vivado_hls_with_period() {
	suffix=$1
	for period in $(echo ${TARGET_PERIOD} | tr -s ':' ' ')
	do
		prefix=$(echo $period | tr -s '.' '_')
		prj=${suffix}_${prefix}
		echo $prj
		echo "target period" ${period}
		echo "PROJ=${prj} PERIOD=${period} vivado_hls -f run_hls.tcl"
		PROJ=${prj} PERIOD=${period} vivado_hls -f run_hls.tcl
	done
}

function run_vivado_hls() {
	echo "running VivadoHLS in $1"
	source $1/settings64.sh
	tmp=( $(echo $i | tr -s '/' ' ') )
	i=$(expr ${#tmp[@]} - 1)
	suffix=$(echo ${tmp[${i}]} | tr -s '.' '_')
	prj=${TARGET}_${suffix}
	run_vivado_hls_with_period ${prj}
}

for i in ${VIVADO}/*
do
	run_vivado_hls $i
done

if type python > /dev/null 2>&1; then
	python tools/analysis.py */solution1/syn/report/${TARGET}_csynth.xml 
fi

