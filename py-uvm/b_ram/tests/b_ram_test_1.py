import os
import sys
import cocotb
import logging
from cocotb.result import TestFailure
from cocotb.result import TestSuccess
from cocotb.clock import Clock
from cocotb.triggers import Timer , RisingEdge
from AXI4_MASTER_Driver import AXI4_master
import b_ram_predefined_signals as up

CLK_PERIOD = 10
def setup_dut(dut):
	cocotb.fork(Clock(dut.CLK, CLK_PERIOD).start())
"""
address = address of the first transfer in a write burst transaction in uart case

no_of_beats_in_burst = the exact number of transfers or beats in a burst . 

size_of_beat_in_bytes = the size(in bytes) of each transfer or beats in the burst.
in case uart

data = the data to be written on the memory

last_beat_of_burst= True (indicates the last transfer in a write burst)
				  = False (indicates the not last transfer in a write burst)

"""

@cocotb.test(skip = False)
def write_read(dut):

	setup_dut(dut)
	dut.RST_N <= 0
	yield Timer(CLK_PERIOD * 10)
	axim = AXI4_master(dut, "axi_slave_slave", dut.CLK)
	
	dut.RST_N <= 1
	yield Timer(CLK_PERIOD)
	
	"""
	setting the mem_address (0) = 5
	"""
	address = 0
	no_of_beats_in_burst = 1 
	size_of_beat_in_bytes = 1
	

	yield axim._send_write_address(address,up.AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info(" address(0) was read by slave")

	
	data = 0x0005
	last_beat_of_burst = True
	
	yield axim._send_write_data(data,up.WID,up.Baud_WSTRB,last_beat_of_burst)
	dut.log.info(" data was read by slave")


	_BRESP = yield axim._get_write_response()
	dut.log.info("the value of BRESP  = %s" %_BRESP)
	yield Timer(CLK_PERIOD * 10)
	"""
	reading back the data from the Baudreg
	"""
	no_of_beats_in_burst = 1 
	size_of_beat_in_bytes = 1


	yield axim._send_Read_address(address,up.AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info(" address(0) was read by slave")

	_RDATA=yield axim._get_Read_data()
	if int(str(_RDATA)[0:16] , 2) == int(data) :
		dut.log.info("the value  = %d" %int(str(_RDATA)[0:8] , 2))	
	else:
		raise TestFailure("Data read  is incorrect %d "%int(str(_RDATA)[0:8] , 2))




