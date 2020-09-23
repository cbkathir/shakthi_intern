import os
import sys
import cocotb
import logging
from cocotb.result import TestFailure
from cocotb.result import TestSuccess
from cocotb.clock import Clock
from cocotb.triggers import Timer , RisingEdge

CLK_PERIOD = 10
def setup_dut(dut):
	cocotb.fork(Clock(dut.CLK, CLK_PERIOD).start())

@cocotb.test(skip = False)
def write_data_on_to_BaudReg(dut):
	"""
	To wite data on to baud reg, the Transaction with the DUT happen within the test (no use of AXI4 driver)
	"""
	setup_dut(dut)
	"""
	De-asserting all the signals
	"""
	dut.AWADDR <= 0
	dut.AWID <= 0
	dut.AWPROT <= 0
	dut.AWLEN <= 0
	dut.AWSIZE <= 0     
	dut.AWBURST <= 0 
	dut.AWVALID <= 0
	dut.WVALID <= 0
	dut.WDATA <= 0
	dut.WID <= 0
	dut.WSTRB <= 0
	dut.WLAST <= 0
	dut.BREADY <= 0

	dut.SIN <= 0

	dut.RVALID <= 0
	dut.RDATA <= 0
	dut.ARVALID <= 0
	dut.RREADY <= 0
	dut.ARSIZE <= 0
	dut.ARADDR <= 0
	dut.ARPROT <= 0
	dut.ARBURST <= 0
	dut.ARLEN <= 0
	dut.ARID <= 0

	dut.RST_N <= 0
	yield Timer(CLK_PERIOD * 10)
	dut.RST_N <= 1
	"""
	setting the write address channel signal
	"""	
	while True:
		yield RisingEdge(dut.CLK)
		if dut.AWREADY == 1:
			dut.log.info("slave ready accept the address")
			break
	dut.AWADDR <= 0x20000
	dut.AWID <= 0b0001
	dut.AWPROT <= 0b000
	dut.AWLEN <= 0x00
	dut.AWSIZE <= 0b001
	dut.AWBURST <= 0b00
	dut.AWVALID <=1
	"""
	setting the write data channel signal
	"""
	while True:
		yield RisingEdge(dut.CLK)
		if dut.WREADY == 1:
			dut.log.info("slave ready accept the data")
			break
	dut.WVALID <= 1
	dut.WDATA <= 0x0005
	dut.WID <= 0b0001
	dut.WSTRB <= 0x03
	dut.WLAST <= 1
	"""
	checking write response signal
	"""
	dut.BREADY <= 1
	while True:
		yield RisingEdge(dut.CLK)
		if dut.BVALID == 1:
			dut.log.info("valid write response is available")	
			break

	
	dut.log.info("THE VALUE OF THE BRESP = %s"%(dut.BRESP))
	if int(dut.BID) == int(dut.AWID):
		dut.log.info("BID value match the AWID value of the write transaction to which the slave is responding")

	else:
		print("BID value didn't match the AWID value of the write transaction to which the slave is responding")
	yield Timer(CLK_PERIOD * 10)
	while True:
		yield RisingEdge(dut.CLK)
		if dut.ARREADY == 1:
			dut.log.info("slave ready accept the address")
			break
	"""
	setting the read address channel signal
	"""
	dut.ARADDR <= 0x20000
	dut.ARSIZE <= 0b001
	dut.ARPROT <= 0b000
	dut.ARLEN <= 0x00
	dut.ARBURST <= 0b00
	dut.ARID <= 0
	dut.ARVALID <= 1

	while True:
		yield RisingEdge(dut.CLK)
		if dut.RVALID == 1:
			dut.log.info("slave ready send the data")
			break
	dut.RREADY <= 1
	R_data = dut.RDATA
	if int((str(R_data)[0:16]),2) == int(0x0005) :
		dut.log.info("data read is correct = %d" %int((str(R_data)[0:16]),2))
	else:
		dut.log.info("data read is correct = %d" %int((str(R_data)[0:16]),2))

	










