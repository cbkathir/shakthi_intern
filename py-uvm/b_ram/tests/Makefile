# Copyright (c) 2016 Technische Universitaet Dresden, Germany
# Chair for VLSI-Design, Diagnostic and Architecture
# Author: Martin Zabel
# All rights reserved.

TOPLEVEL_LANG ?= verilog

COCOTB_EX =/home/cbkathir/py-uvm/cocotb/

PWD=$(shell pwd)

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(WPWD)/../model;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(WPWD)/../hdl/*.v
else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(WPWD)/../hdl/*.vhdl
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif
# VERILOG_SOURCES+=/tools/Bluespec-2018.10.beta1/lib/Verilog/*.vhdl

TOPLEVEL := mkdummy
MODULE   := b_ram_test_1
include $(COCOTB_EX)/makefiles/Makefile.inc
include $(COCOTB_EX)/makefiles/Makefile.sim
