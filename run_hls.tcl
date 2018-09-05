open_project -reset $env(PROJ)
set_top $env(TARGET)
add_files [glob ./sources/*.{cpp,h,c}]
add_files -tb [glob ./testbench/*.{cpp,h,c}]
open_solution -reset solution1
set_part {xc7vx690tffg1761-3}
create_clock -period $env(PERIOD) -name default
# source "./directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog -version $env(VERSION)
quit
