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
	array=$2
	for period in $(echo ${TARGET_PERIOD} | tr -s ':' ' ')
	do
		prefix=$(echo $period | tr -s '.' '_')
		prj=${suffix}_${prefix}
		echo "target period" ${period}
		echo "PROJ=${prj} PERIOD=${period} vivado_hls -f run_hls.tcl"
		PROJ=${prj} PERIOD=${period} vivado_hls -f run_hls.tcl
		array+=(${prj}) 
	done
}

function run_vivado_hls() {
	array=$2
	echo "running VivadoHLS in $1"
	source $1/settings64.sh
	tmp=( $(echo $1 | tr -s '/' ' ') )
	idx=$(expr ${#tmp[@]} - 1)
	suffix=$(echo ${tmp[${idx}]} | tr -s '.' '_')
	prj=${TARGET}_${suffix}
	run_vivado_hls_with_period ${prj} ${array}
}

array=()
for i in ${VIVADO}/*
do
	run_vivado_hls ${i} ${array}
done

if type python > /dev/null 2>&1; then
	rpt=()
	for i in ${array[@]}
	do
		rpt+=($i/solution1/syn/report/${TARGET}_csynth.xml)
	done
	python tools/analysis.py ${rpt[@]}
fi

