import os
import sys
import cocotb
import logging
from cocotb.result import TestFailure
from cocotb.result import TestSuccess
from cocotb.clock import Clock
from cocotb.triggers import Timer , RisingEdge
from AXI4_MASTER_Driver import AXI4_master
import uart_predefined_signals as up

CLK_PERIOD = 10
def setup_dut(dut):
	cocotb.fork(Clock(dut.CLK, CLK_PERIOD).start())
"""
address = address of the first transfer in a write burst transaction in uart case
Baudreg = 0x20000
rxreg = 0x20004
txreg = 0x20008
statusreg = 0x2000c

no_of_beats_in_burst = the exact number of transfers or beats in a burst . 
in uart case
1)for Baudreg the value is 1
2)for rxreg,txreg the values are 1,2,3 

size_of_beat_in_bytes = the size(in bytes) of each transfer or beats in the burst.
in case uart
 BaudReg      2 bytes(16-bit) Register to change the baud-value of the UART.
 RxReg        1 byte (8-bit) register to read the incoming value.
 TxReg        1 byte (8-bit) register to be written to send data out.
 StatusReg    The 4-bit register capturing the status of the rx/tx user side FIFOs  (doubt ????)

data = the data to be written on the memory

burst_type = simple uart supports only FIXED burst.
			 This burst type is used for repeated accesses to the same location such as when loading or emptying a FIFO

last_beat_of_burst= True (indicates the last transfer in a write burst)
				  = False (indicates the not last transfer in a write burst)

"""

@cocotb.test(skip = False)
def slave_error(dut):
	"""
	To check slave error
	"""
	setup_dut(dut)
	axim = AXI4_master(dut, None, dut.CLK)
	
	dut.RST_N <= 0
	yield Timer(CLK_PERIOD * 10)
	dut.RST_N <= 1

	"""
	setting the Baudrate (0x20000) = 0
	"""
	"""
	sending the write address and data to the AXI4 master driver
	"""
	address = 0x20000
	no_of_beats_in_burst = 1
	size_of_beat_in_bytes = 2
	data=[0]
	AxID=2
	WID=2
	_BRESP = yield axim.write_transaction(address,AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type,data,WID)
	dut.log.info("the value of BRESP of write transaction at address %d = %s" %(address ,_BRESP))

	address = 0x20000
	no_of_beats_in_burst = 1
	size_of_beat_in_bytes = 2
	AxID=3
	d=yield axim.read_transaction(address,AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Burst of beat %d at address(%d) was read by slave" %(no_of_beats_in_burst,address))
	for t in range(no_of_beats_in_burst):
		dut.log.info(" data = %d" %int((str(d[t])[0:16]),2))

	"""
	settting Rxreg(0x20004)
	"""
	"""
	sending the write address and data to the AXI4 master driver
	"""
	address = 0x20004
	no_of_beats_in_burst = 3
	size_of_beat_in_bytes = 1
	data=[61,62,63]
	AxID=2
	WID=2
	_BRESP = yield axim.write_transaction(address,AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type,data,WID)
	dut.log.info("the value of BRESP of write transaction at address %d = %s" %(address ,_BRESP))

	yield Timer(CLK_PERIOD * 600)
	
	"""
	reading back the data from the Txreg
	"""
	"""
	sending the read address to AXI4 master driver to read back data
	"""
	address = 0x20008
	no_of_beats_in_burst = 3
	size_of_beat_in_bytes = 1
	AxID=3
	d=yield axim.read_transaction(address,AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Burst of beat %d at address(%d) was read by slave" %(no_of_beats_in_burst,address))
	for t in range(no_of_beats_in_burst):
		dut.log.info(" data = %d" %int((str(d[t])[0:8]),2))
	if int(str(_BRESP),2)==2:
		raise TestFailure('Even though Write response = 10 (Slave Error) was dedected ,side effect was observed')

