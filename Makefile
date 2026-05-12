# Simulator selection
SIM ?= icarus

# Hardware description language
TOPLEVEL_LANG ?= verilog

# Verilog source files
VERILOG_SOURCES += $(PWD)/src/rgb2gray.sv

# Flag to enable SystemVerilog support in Icarus
COMPILE_ARGS += -g2012

# Top-level module name in SystemVerilog
TOPLEVEL = rgb2gray

# Testbench Python file name (without .py)
MODULE = test_rgb2gray

# Path to the testbench directory
export PYTHONPATH := $(PWD)/tb:$(PYTHONPATH)

# Invoke the Cocotb core makefile
include $(shell cocotb-config --makefiles)/Makefile.sim